export type NotificationChannel = 'email' | 'sms' | 'in_app';

export interface NotificationSendEvent {
  eventType: 'notification.send';
  recipientId: string;
  recipientEmail?: string;
  recipientPhone?: string;
  channels: NotificationChannel[];
  subject: string;
  body: string;
  metadata?: Record<string, unknown>;
  triggeredAt: string;
}

export type NotificationEvent = NotificationSendEvent;
