import amqplib, { Channel, ChannelModel, Options } from 'amqplib';
import { BINDINGS, EXCHANGES, QUEUES } from './topology';

export interface RabbitMQConfig {
  host: string;
  port: number;
  username: string;
  password: string;
  vhost: string;
}

export interface PublishOptions {
  priority?: number;
  correlationId?: string;
  replyTo?: string;
  expiration?: string;
}

function buildUrl(config: RabbitMQConfig): string {
  const { host, port, username, password, vhost } = config;
  return `amqp://${username}:${password}@${host}:${port}/${encodeURIComponent(vhost)}`;
}

function configFromEnv(): RabbitMQConfig {
  return {
    host:     process.env.RABBITMQ_HOST     ?? 'localhost',
    port:     parseInt(process.env.RABBITMQ_PORT ?? '5672', 10),
    username: process.env.RABBITMQ_USER     ?? 'guest',
    password: process.env.RABBITMQ_PASSWORD ?? 'guest',
    vhost:    process.env.RABBITMQ_VHOST    ?? '/',
  };
}

export class RabbitMQClient {
  private connection: ChannelModel | null = null;
  private channel: Channel | null = null;
  private readonly config: RabbitMQConfig;
  private readonly maxRetries: number;
  private readonly retryDelayMs: number;

  constructor(config?: RabbitMQConfig, maxRetries = 5, retryDelayMs = 3000) {
    this.config = config ?? configFromEnv();
    this.maxRetries = maxRetries;
    this.retryDelayMs = retryDelayMs;
  }

  async connect(): Promise<void> {
    const url = buildUrl(this.config);
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        const conn = await amqplib.connect(url);
        this.connection = conn;
        this.channel = await conn.createChannel();
        await this.channel.prefetch(1);

        conn.on('error', (err: Error) => {
          console.error('[RabbitMQ] Connection error:', err.message);
        });
        conn.on('close', () => {
          console.warn('[RabbitMQ] Connection closed');
          this.connection = null;
          this.channel = null;
        });

        console.log('[RabbitMQ] Connected');
        return;
      } catch (err) {
        console.error(`[RabbitMQ] Attempt ${attempt}/${this.maxRetries} failed: ${(err as Error).message}`);
        if (attempt < this.maxRetries) {
          await this.delay(this.retryDelayMs);
        } else {
          throw new Error(`[RabbitMQ] Failed to connect after ${this.maxRetries} attempts`);
        }
      }
    }
  }

  /** Declare all exchanges, queues, and bindings. Idempotent. */
  async setupTopology(): Promise<void> {
    const ch = this.getChannel();

    // Dead-letter exchange first
    await ch.assertExchange(EXCHANGES.DEAD_LETTER.name, EXCHANGES.DEAD_LETTER.type, { durable: true });

    for (const ex of Object.values(EXCHANGES)) {
      if (ex.name === EXCHANGES.DEAD_LETTER.name) continue;
      await ch.assertExchange(ex.name, ex.type, { durable: ex.durable });
    }

    for (const q of Object.values(QUEUES)) {
      const opts: Options.AssertQueue = { durable: q.durable };
      if (q.deadLetterExchange) opts.deadLetterExchange = q.deadLetterExchange;
      if (q.messageTtl)         opts.messageTtl = q.messageTtl;
      await ch.assertQueue(q.name, opts);
    }

    for (const b of BINDINGS) {
      await ch.bindQueue(b.queue, b.exchange, b.routingKey);
    }

    console.log('[RabbitMQ] Topology setup complete');
  }

  /** Publish an event with persistent delivery. */
  async publish<T extends { eventType: string }>(
    exchange: string,
    routingKey: string,
    event: T,
    options: PublishOptions = {},
  ): Promise<void> {
    const ch = this.getChannel();
    const content = Buffer.from(JSON.stringify(event));
    ch.publish(exchange, routingKey, content, {
      persistent: true,
      contentType: 'application/json',
      timestamp: Date.now(),
      ...options,
    });
  }

  /** Subscribe to a queue. Acks on success, nacks to DLX on error. */
  async subscribe<T>(queue: string, handler: (message: T) => Promise<void>): Promise<void> {
    const ch = this.getChannel();
    await ch.consume(queue, async (msg: amqplib.ConsumeMessage | null) => {
      if (!msg) return;
      try {
        const content = JSON.parse(msg.content.toString()) as T;
        await handler(content);
        ch.ack(msg);
      } catch (err) {
        console.error(`[RabbitMQ] Error processing message from ${queue}:`, (err as Error).message);
        ch.nack(msg, false, false);
      }
    });
    console.log(`[RabbitMQ] Subscribed to: ${queue}`);
  }

  async close(): Promise<void> {
    try {
      await this.channel?.close();
      await this.connection?.close();
      console.log('[RabbitMQ] Closed gracefully');
    } catch (err) {
      console.error('[RabbitMQ] Error closing:', (err as Error).message);
    } finally {
      this.channel = null;
      this.connection = null;
    }
  }

  isConnected(): boolean {
    return this.connection !== null && this.channel !== null;
  }

  private getChannel(): Channel {
    if (!this.channel) throw new Error('[RabbitMQ] Not connected. Call connect() first.');
    return this.channel;
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
