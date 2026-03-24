export interface ResourceScheduledEvent {
  eventType: 'resource.scheduled';
  resourceId: string;
  taskId: string;
  scheduledStart: string;
  scheduledEnd: string;
}

export interface ResourceUnavailableEvent {
  eventType: 'resource.unavailable';
  resourceId: string;
  reason: string;
  unavailableFrom: string;
  unavailableUntil?: string;
}

export type ResourceEvent = ResourceScheduledEvent | ResourceUnavailableEvent;
