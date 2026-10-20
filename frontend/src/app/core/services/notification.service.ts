import { Injectable, signal } from '@angular/core';

export type NotificationType = 'success' | 'error';

export interface Notification {
  id: number;
  type: NotificationType;
  message: string;
}

/** Estado global de los avisos (toasts). Cualquier parte de la app puede publicar uno. */
@Injectable({ providedIn: 'root' })
export class NotificationService {
  private nextId = 1;
  private readonly items = signal<Notification[]>([]);

  /** Solo lectura hacia afuera: nadie más puede modificar la lista directamente. */
  readonly notifications = this.items.asReadonly();

  success(message: string): void {
    this.show('success', message);
  }

  error(message: string): void {
    this.show('error', message);
  }

  dismiss(id: number): void {
    this.items.update((list) => list.filter((n) => n.id !== id));
  }

  private show(type: NotificationType, message: string, durationMs = 4000): void {
    const id = this.nextId++;
    this.items.update((list) => [...list, { id, type, message }]);
    setTimeout(() => this.dismiss(id), durationMs);
  }
}
