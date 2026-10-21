import { Component, input, output } from '@angular/core';

import { Task } from '../../../core/models/task.model';
import { StatusChange, TaskCard } from '../task-card/task-card';

// pinta las tarjetas (o el mensaje de vacio) y pasa hacia arriba lo que emite cada una
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
