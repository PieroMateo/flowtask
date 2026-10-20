import { DatePipe } from '@angular/common';
import { Component, computed, input, output } from '@angular/core';

import { Task, TaskStatus } from '../../../core/models/task.model';

export interface StatusChange {
  task: Task;
  status: TaskStatus;
}

const STATUS_BADGE: Record<TaskStatus, string> = {
  Pendiente: 'bg-amber-100 text-amber-800',
  'En Progreso': 'bg-sky-100 text-sky-800',
  Completada: 'bg-emerald-100 text-emerald-800',
};

/** Fecha de hoy en formato "YYYY-MM-DD" según la hora LOCAL (toISOString usaría UTC). */
function todayIso(): string {
  const d = new Date();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${month}-${day}`;
}

/** Presentacional: muestra una tarea y avisa al padre cuando el usuario quiere cambiarla. */
@Component({
  selector: 'app-task-card',
  imports: [DatePipe],
  templateUrl: './task-card.html',
})
export class TaskCard {
  readonly task = input.required<Task>();
  /** true mientras hay una petición en curso para esta tarea (evita doble clic). */
  readonly busy = input(false);

  readonly statusChange = output<StatusChange>();
  readonly remove = output<Task>();

  protected readonly isCompleted = computed(() => this.task().status === 'Completada');
  // Las fechas ISO se pueden comparar como texto: "2026-10-19" < "2026-10-20".
  protected readonly isOverdue = computed(
    () => !this.isCompleted() && this.task().due_date < todayIso(),
  );
  protected readonly badgeClasses = computed(() => STATUS_BADGE[this.task().status]);

  protected changeStatus(status: TaskStatus): void {
    this.statusChange.emit({ task: this.task(), status });
  }
}
