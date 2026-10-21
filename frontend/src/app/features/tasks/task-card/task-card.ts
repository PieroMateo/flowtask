import { DatePipe } from '@angular/common';
import { Component, computed, input, output } from '@angular/core';

import { Task, TaskStatus } from '../../../core/models/task.model';

export interface StatusChange {
  task: Task;
  status: TaskStatus;
}

// colores de la etiqueta de cada estado
const STATUS_BADGE: Record<TaskStatus, string> = {
  Pendiente: 'bg-amber-100 text-amber-800',
  'En Progreso': 'bg-sky-100 text-sky-800',
  Completada: 'bg-emerald-100 text-emerald-800',
};

// fecha de hoy como "YYYY-MM-DD" en hora local. con toISOString saldria en UTC
// y en Peru a partir de las 7pm ya daria el dia siguiente
function todayIso(): string {
  const d = new Date();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${month}-${day}`;
}

// solo muestra la tarea y avisa al padre, no llama al backend
@Component({
  selector: 'app-task-card',
  imports: [DatePipe],
  templateUrl: './task-card.html',
})
export class TaskCard {
  readonly task = input.required<Task>();
  // mientras hay una peticion en curso los botones se bloquean, evita el doble clic
  readonly busy = input(false);

  readonly statusChange = output<StatusChange>();
  readonly remove = output<Task>();

  protected readonly isCompleted = computed(() => this.task().status === 'Completada');
  // con el formato YYYY-MM-DD se pueden comparar como texto
  protected readonly isOverdue = computed(
    () => !this.isCompleted() && this.task().due_date < todayIso(),
  );
  protected readonly badgeClasses = computed(() => STATUS_BADGE[this.task().status]);

  protected changeStatus(status: TaskStatus): void {
    this.statusChange.emit({ task: this.task(), status });
  }
}
