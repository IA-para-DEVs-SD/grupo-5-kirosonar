/**
 * RabbitMQ Exchange and Queue Topology
 * All exchanges are topic exchanges for flexible routing.
 * All queues and messages are durable/persistent for reliability.
 */

export interface ExchangeConfig {
  name: string;
  type: 'topic' | 'direct' | 'fanout';
  durable: boolean;
}

export interface QueueConfig {
  name: string;
  durable: boolean;
  deadLetterExchange?: string;
  messageTtl?: number;
}

export interface BindingConfig {
  queue: string;
  exchange: string;
  routingKey: string;
}

// ─── Exchanges ────────────────────────────────────────────────────────────────

export const EXCHANGES: Record<string, ExchangeConfig> = {
  ORDERS:        { name: 'erp.orders',        type: 'topic', durable: true },
  PRODUCTION:    { name: 'erp.production',    type: 'topic', durable: true },
  MATERIALS:     { name: 'erp.materials',     type: 'topic', durable: true },
  RESOURCES:     { name: 'erp.resources',     type: 'topic', durable: true },
  QUALITY:       { name: 'erp.quality',       type: 'topic', durable: true },
  DELIVERY:      { name: 'erp.delivery',      type: 'topic', durable: true },
  FINANCIAL:     { name: 'erp.financial',     type: 'topic', durable: true },
  NOTIFICATIONS: { name: 'erp.notifications', type: 'topic', durable: true },
  DEAD_LETTER:   { name: 'erp.dead_letter',   type: 'topic', durable: true },
};

// ─── Routing Keys ─────────────────────────────────────────────────────────────

export const ROUTING_KEYS = {
  ORDER_CREATED:              'order.created',
  ORDER_UPDATED:              'order.updated',
  ORDER_CONFIRMED:            'order.confirmed',
  ORDER_COMPLETED:            'order.completed',
  PRODUCTION_ORDER_CREATED:   'production.order.created',
  PRODUCTION_TASK_STARTED:    'production.task.started',
  PRODUCTION_TASK_COMPLETED:  'production.task.completed',
  MATERIAL_RESERVED:          'material.reserved',
  MATERIAL_CONSUMED:          'material.consumed',
  MATERIAL_LOW_STOCK:         'material.low_stock',
  RESOURCE_SCHEDULED:         'resource.scheduled',
  RESOURCE_UNAVAILABLE:       'resource.unavailable',
  QUALITY_APPROVED:           'quality.approved',
  QUALITY_REJECTED:           'quality.rejected',
  DELIVERY_STARTED:           'delivery.started',
  DELIVERY_COMPLETED:         'delivery.completed',
  DELIVERY_DELAYED:           'delivery.delayed',
  INVOICE_GENERATED:          'invoice.generated',
  PAYMENT_RECEIVED:           'payment.received',
  NOTIFICATION_SEND:          'notification.send',
} as const;

export type RoutingKey = (typeof ROUTING_KEYS)[keyof typeof ROUTING_KEYS];

// ─── Queues ───────────────────────────────────────────────────────────────────

const DLX = EXCHANGES.DEAD_LETTER.name;

export const QUEUES: Record<string, QueueConfig> = {
  ORDER_SERVICE_EVENTS:                  { name: 'order-service.events',                  durable: true, deadLetterExchange: DLX },
  PRODUCTION_SERVICE_ORDER_EVENTS:       { name: 'production-service.order-events',       durable: true, deadLetterExchange: DLX },
  PRODUCTION_SERVICE_RESOURCE_EVENTS:    { name: 'production-service.resource-events',    durable: true, deadLetterExchange: DLX },
  PRODUCTION_SERVICE_QUALITY_EVENTS:     { name: 'production-service.quality-events',     durable: true, deadLetterExchange: DLX },
  MATERIAL_SERVICE_ORDER_EVENTS:         { name: 'material-service.order-events',         durable: true, deadLetterExchange: DLX },
  MATERIAL_SERVICE_PRODUCTION_EVENTS:    { name: 'material-service.production-events',    durable: true, deadLetterExchange: DLX },
  RESOURCE_SERVICE_PRODUCTION_EVENTS:    { name: 'resource-service.production-events',    durable: true, deadLetterExchange: DLX },
  QUALITY_SERVICE_PRODUCTION_EVENTS:     { name: 'quality-service.production-events',     durable: true, deadLetterExchange: DLX },
  FINANCIAL_SERVICE_ORDER_EVENTS:        { name: 'financial-service.order-events',        durable: true, deadLetterExchange: DLX },
  DELIVERY_SERVICE_ORDER_EVENTS:         { name: 'delivery-service.order-events',         durable: true, deadLetterExchange: DLX },
  NOTIFICATION_SERVICE_EVENTS:           { name: 'notification-service.events',           durable: true, deadLetterExchange: DLX },
  REPORTING_SERVICE_EVENTS:              { name: 'reporting-service.events',              durable: true, deadLetterExchange: DLX },
  DEAD_LETTER:                           { name: 'erp.dead_letter',                       durable: true },
};

// ─── Bindings ─────────────────────────────────────────────────────────────────

export const BINDINGS: BindingConfig[] = [
  // Production Service ← Orders
  { queue: QUEUES.PRODUCTION_SERVICE_ORDER_EVENTS.name,    exchange: EXCHANGES.ORDERS.name,     routingKey: 'order.confirmed' },
  { queue: QUEUES.PRODUCTION_SERVICE_ORDER_EVENTS.name,    exchange: EXCHANGES.ORDERS.name,     routingKey: 'order.updated' },
  // Production Service ← Resources
  { queue: QUEUES.PRODUCTION_SERVICE_RESOURCE_EVENTS.name, exchange: EXCHANGES.RESOURCES.name,  routingKey: 'resource.unavailable' },
  // Production Service ← Quality
  { queue: QUEUES.PRODUCTION_SERVICE_QUALITY_EVENTS.name,  exchange: EXCHANGES.QUALITY.name,    routingKey: 'quality.approved' },
  { queue: QUEUES.PRODUCTION_SERVICE_QUALITY_EVENTS.name,  exchange: EXCHANGES.QUALITY.name,    routingKey: 'quality.rejected' },
  // Material Service ← Orders
  { queue: QUEUES.MATERIAL_SERVICE_ORDER_EVENTS.name,      exchange: EXCHANGES.ORDERS.name,     routingKey: 'order.confirmed' },
  // Material Service ← Production
  { queue: QUEUES.MATERIAL_SERVICE_PRODUCTION_EVENTS.name, exchange: EXCHANGES.PRODUCTION.name, routingKey: 'production.task.completed' },
  // Resource Service ← Production
  { queue: QUEUES.RESOURCE_SERVICE_PRODUCTION_EVENTS.name, exchange: EXCHANGES.PRODUCTION.name, routingKey: 'production.order.created' },
  { queue: QUEUES.RESOURCE_SERVICE_PRODUCTION_EVENTS.name, exchange: EXCHANGES.PRODUCTION.name, routingKey: 'production.task.completed' },
  // Quality Service ← Production
  { queue: QUEUES.QUALITY_SERVICE_PRODUCTION_EVENTS.name,  exchange: EXCHANGES.PRODUCTION.name, routingKey: 'production.task.completed' },
  // Financial Service ← Orders
  { queue: QUEUES.FINANCIAL_SERVICE_ORDER_EVENTS.name,     exchange: EXCHANGES.ORDERS.name,     routingKey: 'order.completed' },
  // Delivery Service ← Orders
  { queue: QUEUES.DELIVERY_SERVICE_ORDER_EVENTS.name,      exchange: EXCHANGES.ORDERS.name,     routingKey: 'order.completed' },
  // Notification Service
  { queue: QUEUES.NOTIFICATION_SERVICE_EVENTS.name,        exchange: EXCHANGES.NOTIFICATIONS.name, routingKey: 'notification.send' },
  { queue: QUEUES.NOTIFICATION_SERVICE_EVENTS.name,        exchange: EXCHANGES.MATERIALS.name,  routingKey: 'material.low_stock' },
  { queue: QUEUES.NOTIFICATION_SERVICE_EVENTS.name,        exchange: EXCHANGES.DELIVERY.name,   routingKey: 'delivery.delayed' },
  { queue: QUEUES.NOTIFICATION_SERVICE_EVENTS.name,        exchange: EXCHANGES.QUALITY.name,    routingKey: 'quality.rejected' },
  // Reporting Service ← all events (wildcard)
  { queue: QUEUES.REPORTING_SERVICE_EVENTS.name,           exchange: EXCHANGES.ORDERS.name,     routingKey: 'order.#' },
  { queue: QUEUES.REPORTING_SERVICE_EVENTS.name,           exchange: EXCHANGES.PRODUCTION.name, routingKey: 'production.#' },
  { queue: QUEUES.REPORTING_SERVICE_EVENTS.name,           exchange: EXCHANGES.MATERIALS.name,  routingKey: 'material.#' },
  { queue: QUEUES.REPORTING_SERVICE_EVENTS.name,           exchange: EXCHANGES.FINANCIAL.name,  routingKey: '#' },
  { queue: QUEUES.REPORTING_SERVICE_EVENTS.name,           exchange: EXCHANGES.DELIVERY.name,   routingKey: 'delivery.#' },
];
