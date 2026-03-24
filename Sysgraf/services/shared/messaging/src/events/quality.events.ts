export interface QualityApprovedEvent {
  eventType: 'quality.approved';
  qualityCheckId: string;
  productionOrderId: string;
  inspectorId: string;
  approvedAt: string;
}

export interface QualityRejectedEvent {
  eventType: 'quality.rejected';
  qualityCheckId: string;
  productionOrderId: string;
  inspectorId: string;
  defectType: string;
  defectDescription: string;
  rejectedAt: string;
}

export type QualityEvent = QualityApprovedEvent | QualityRejectedEvent;
