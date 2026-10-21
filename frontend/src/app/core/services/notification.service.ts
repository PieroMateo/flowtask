import { Injectable, signal } from '@angular/core';

export type NotificationType = 'success' | 'error';

export interface Notification {
  id: number;
  type: NotificationType;
  message: string;
}

// guarda los avisos que salen abajo a la derecha, cualquier parte de la app puede mandar uno
@Injectable({ providedIn: 'root' })
export class NotificationService {
  private nextId = 1;
  private readonly items = signal<Notification[]>([]);

  // hacia afuera solo se puede leer, para agregar o quitar hay que usar los metodos de abajo
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
    // arreglo nuevo en vez de push, si no la signal no detecta el cambio
    this.items.update((list) => [...list, { id, type, message }]);
    setTimeout(() => this.dismiss(id), durationMs);
  }
}
