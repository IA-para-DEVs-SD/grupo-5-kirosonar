/**
 * Bootstrap script: connects to RabbitMQ and sets up the full topology.
 * Run once after `docker compose up` to declare all exchanges, queues, and bindings.
 */
import { RabbitMQClient } from './connection';

async function main(): Promise<void> {
  const client = new RabbitMQClient();
  try {
    await client.connect();
    await client.setupTopology();
    console.log('Messaging topology initialized successfully.');
  } finally {
    await client.close();
  }
}

main().catch((err) => {
  console.error('Setup failed:', err);
  process.exit(1);
});
