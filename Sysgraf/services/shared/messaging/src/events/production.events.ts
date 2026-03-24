export interface ProductionOrderCreatedEvent {
  eventType: 'production.order.created';
  productionOrderId: string;
  orderId: string;
  productionNumber: string;
  createdAt: string;
}

export interface ProductionTaskStartedEvent {
  eventType: 'production.task.started';
  taskId: string;
  productionOrderId: string;
  taskType: string;
  startedAt: string;
}

export interface ProductionTaskCompletedEvent {
  eventType: 'production.task.completed';
  taskId: string;
  productionOrderId: string;
  taskType: string;
  completedAt: string;
  durationMinutes: number;
}

export type ProductionEvent =
  | ProductionOrderCreatedEvent
  | ProductionTaskStartedEvent
  | ProductionTaskCompletedEvent;
