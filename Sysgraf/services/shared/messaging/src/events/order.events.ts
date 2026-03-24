export interface OrderCreatedEvent {
  eventType: 'order.created';
  orderId: string;
  customerId: string;
  orderNumber: string;
  createdAt: string;
}

export interface OrderUpdatedEvent {
  eventType: 'order.updated';
  orderId: string;
  changes: Record<string, unknown>;
  updatedAt: string;
}

export interface OrderConfirmedEvent {
  eventType: 'order.confirmed';
  orderId: string;
  customerId: string;
  orderNumber: string;
  confirmedAt: string;
}

export interface OrderCompletedEvent {
  eventType: 'order.completed';
  orderId: string;
  customerId: string;
  orderNumber: string;
  completedAt: string;
  totalAmount: number;
}

export type OrderEvent =
  | OrderCreatedEvent
  | OrderUpdatedEvent
  | OrderConfirmedEvent
  | OrderCompletedEvent;
