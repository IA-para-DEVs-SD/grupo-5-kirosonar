export interface DeliveryStartedEvent {
  eventType: 'delivery.started';
  deliveryId: string;
  orderId: string;
  trackingCode: string;
  startedAt: string;
}

export interface DeliveryCompletedEvent {
  eventType: 'delivery.completed';
  deliveryId: string;
  orderId: string;
  trackingCode: string;
  deliveredAt: string;
  deliveredBy: string;
}

export interface DeliveryDelayedEvent {
  eventType: 'delivery.delayed';
  deliveryId: string;
  orderId: string;
  customerId: string;
  originalDate: string;
  newEstimatedDate: string;
  reason: string;
}

export type DeliveryEvent =
  | DeliveryStartedEvent
  | DeliveryCompletedEvent
  | DeliveryDelayedEvent;
