export interface MaterialReservedEvent {
  eventType: 'material.reserved';
  materialId: string;
  productionOrderId: string;
  quantityReserved: number;
  reservedAt: string;
}

export interface MaterialConsumedEvent {
  eventType: 'material.consumed';
  materialId: string;
  productionOrderId: string;
  quantityConsumed: number;
  consumedAt: string;
}

export interface MaterialLowStockEvent {
  eventType: 'material.low_stock';
  materialId: string;
  materialName: string;
  currentQuantity: number;
  minimumStock: number;
  triggeredAt: string;
}

export type MaterialEvent =
  | MaterialReservedEvent
  | MaterialConsumedEvent
  | MaterialLowStockEvent;
