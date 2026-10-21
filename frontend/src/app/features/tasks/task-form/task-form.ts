import { Component, inject, input, output, signal } from '@angular/core';
import { NonNullableFormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { Category } from '../../../core/models/category.model';
import { TASK_STATUSES, Task, TaskStatus } from '../../../core/models/task.model';
import { NotificationService } from '../../../core/services/notification.service';
import { TaskService } from '../../../core/services/task.service';

// este si hace su propio POST porque necesita saber cuando termina
// para limpiar el formulario y soltar el boton. al final avisa al board con (created)
@Component({
  selector: 'app-task-form',
  imports: [ReactiveFormsModule],
  templateUrl: './task-form.html',
})
export class TaskForm {
  private readonly fb = inject(NonNullableFormBuilder);
  private readonly taskService = inject(TaskService);
  private readonly notifications = inject(NotificationService);

  readonly categories = input<Category[]>([]);
  readonly created = output<Task>();

  protected readonly statuses = TASK_STATUSES;
  protected readonly submitting = signal(false);

  // con nonNullable el reset() devuelve cada campo a su valor inicial y no a null
  protected readonly form = this.fb.group({
    // el pattern pide al menos un caracter que no sea espacio, igual que en el backend
    title: ['', [Validators.required, Validators.maxLength(150), Validators.pattern(/\S/)]],
    description: [''],
    status: this.fb.control<TaskStatus>('Pendiente'),
    due_date: ['', Validators.required],
    category_id: this.fb.control<number | null>(null, Validators.required),
  });

  // el error de un campo se muestra recien cuando el usuario ya paso por el
  protected showError(field: keyof typeof this.form.controls): boolean {
    const control = this.form.controls[field];
    return control.invalid && (control.touched || control.dirty);
  }

  protected onSubmit(): void {
    if (this.form.invalid) {
      // marca todo como tocado para que aparezcan los mensajes en rojo
      this.form.markAllAsTouched();
      return;
    }

    const value = this.form.getRawValue();
    this.submitting.set(true);
    this.taskService
      .create({
        title: value.title.trim(),
        description: value.description.trim() || null,
        status: value.status,
        due_date: value.due_date,
        category_id: value.category_id!, // aqui ya no puede ser null, lo cubre el required
      })
      .subscribe({
        next: (task) => {
          this.notifications.success(`Tarea "${task.title}" creada`);
          this.form.reset();
          this.submitting.set(false);
          this.created.emit(task);
        },
        // el aviso de error ya lo muestra el interceptor, aqui solo se libera el boton
        error: () => this.submitting.set(false),
      });
  }
}
