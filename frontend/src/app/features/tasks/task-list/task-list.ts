import { Component, input, output } from '@angular/core';

import { Task } from '../../../core/models/task.model';
import { StatusChange, TaskCard } from '../task-card/task-card';

/** Presentacional: dibuja la lista (o su estado vacío) y reenvía los eventos de cada tarjeta. */
@Component({
  selector: 'app-task-list',
  imports: [TaskCard],
  templateUrl: './task-list.html',
})
export class TaskList {
  readonly tasks = input.required<Task[]>();
  readonly loading = input(false);
  readonly busyIds = input<ReadonlySet<number>>(new Set());

  readonly statusChange = output<StatusChange>();
  readonly remove = output<Task>();
}
