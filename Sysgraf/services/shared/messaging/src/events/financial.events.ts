export interface InvoiceGeneratedEvent {
  eventType: 'invoice.generated';
  invoiceId: string;
  orderId: string;
  invoiceNumber: string;
  totalAmount: number;
  dueDate: string;
  generatedAt: string;
}

export interface PaymentReceivedEvent {
  eventType: 'payment.received';
  invoiceId: string;
  orderId: string;
  paidAmount: number;
  paymentMethod: string;
  receivedAt: string;
}

export type FinancialEvent = InvoiceGeneratedEvent | PaymentReceivedEvent;
