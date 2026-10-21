import { Component, OnInit, inject, signal } from '@angular/core';
import { Subscription } from 'rxjs';

import { Category } from '../../../core/models/category.model';
import { Task, TaskFilters } from '../../../core/models/task.model';
import { CategoryService } from '../../../core/services/category.service';
import { NotificationService } from '../../../core/services/notification.service';
import { TaskService } from '../../../core/services/task.service';
import { FilterBar } from '../filter-bar/filter-bar';
import { StatusChange } from '../task-card/task-card';
import { TaskForm } from '../task-form/task-form';
import { TaskList } from '../task-list/task-list';

// el que manda en el tablero: tiene el estado y es el que llama a los servicios
@Component({
  selector: 'app-task-board',
  imports: [FilterBar, TaskForm, TaskList],
  templateUrl: './task-board.html',
})
export class TaskBoard implements OnInit {
  private readonly taskService = inject(TaskService);
  private readonly categoryService = inject(CategoryService);
  private readonly notifications = inject(NotificationService);

  protected readonly tasks = signal<Task[]>([]);
  protected readonly categories = signal<Category[]>([]);
  protected readonly filters = signal<TaskFilters>({});
  protected readonly loading = signal(false);
  protected readonly loadFailed = signal(false);
  // ids de las tareas que estan esperando respuesta del backend
  protected readonly busyIds = signal<ReadonlySet<number>>(new Set());

  private loadSubscription?: Subscription;

  ngOnInit(): void {
    this.loadCategories();
    this.loadTasks();
  }

  protected loadTasks(): void {
    // si se cambia de filtro rapido se cancela la peticion anterior,
    // asi una respuesta vieja no pisa a la nueva
    this.loadSubscription?.unsubscribe();
    this.loading.set(true);
    this.loadFailed.set(false);

    this.loadSubscription = this.taskService.getAll(this.filters()).subscribe({
      next: (tasks) => {
        this.tasks.set(tasks);
        this.loading.set(false);
      },
      error: () => {
        this.loadFailed.set(true);
        this.loading.set(false);
      },
    });
  }

  protected onFiltersChange(filters: TaskFilters): void {
    this.filters.set(filters);
    this.loadTasks();
  }

  protected onTaskCreated(): void {
    // se vuelve a pedir la lista para respetar el filtro y el orden por fecha del backend
    this.loadTasks();
  }

  protected onStatusChange({ task, status }: StatusChange): void {
    this.setBusy(task.id, true);
    this.taskService.updateStatus(task.id, status).subscribe({
      next: (updated) => {
        // si con el nuevo estado ya no entra en el filtro, se saca de la lista
        this.tasks.update((list) =>
          this.matchesFilters(updated)
            ? list.map((t) => (t.id === updated.id ? updated : t))
            : list.filter((t) => t.id !== updated.id),
        );
        this.setBusy(task.id, false);
        this.notifications.success(`"${updated.title}" ahora está ${updated.status}`);
      },
      error: () => this.setBusy(task.id, false),
    });
  }

  protected onRemove(task: Task): void {
    if (!confirm(`¿Eliminar la tarea "${task.title}"?\nEsta acción no se puede deshacer.`)) {
      return;
    }
    this.setBusy(task.id, true);
    this.taskService.delete(task.id).subscribe({
      next: () => {
        this.tasks.update((list) => list.filter((t) => t.id !== task.id));
        this.setBusy(task.id, false);
        this.notifications.success(`Tarea "${task.title}" eliminada`);
      },
      error: () => this.setBusy(task.id, false),
    });
  }

  private loadCategories(): void {
    this.categoryService.getAll().subscribe({
      next: (categories) => this.categories.set(categories),
      error: () => {}, // el aviso ya lo saca el interceptor
    });
  }

  private matchesFilters(task: Task): boolean {
    const { status, categoryId } = this.filters();
    return (!status || task.status === status) && (!categoryId || task.category_id === categoryId);
  }

  private setBusy(id: number, busy: boolean): void {
    // se arma un Set nuevo, si se modifica el mismo la signal no se da cuenta
    this.busyIds.update((ids) => {
      const next = new Set(ids);
      if (busy) next.add(id);
      else next.delete(id);
      return next;
    });
  }
}
