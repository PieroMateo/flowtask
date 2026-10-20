import { Component, inject, input, output, signal } from '@angular/core';
import { NonNullableFormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { Category } from '../../../core/models/category.model';
import { TASK_STATUSES, Task, TaskStatus } from '../../../core/models/task.model';
import { NotificationService } from '../../../core/services/notification.service';
import { TaskService } from '../../../core/services/task.service';

/**
 * Formulario de creación. Es dueño de su propio envío (llama a TaskService) porque así
 * controla su estado "enviando" y su reinicio; al terminar avisa al padre con (created).
 */
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

  // nonNullable: al hacer reset() cada campo vuelve a su valor inicial, no a null.
  protected readonly form = this.fb.group({
    // pattern(/\S/): exige al menos un carácter que no sea espacio (igual que el backend).
    title: ['', [Validators.required, Validators.maxLength(150), Validators.pattern(/\S/)]],
    description: [''],
    status: this.fb.control<TaskStatus>('Pendiente'),
    due_date: ['', Validators.required],
    category_id: this.fb.control<number | null>(null, Validators.required),
  });

  /** Muestra el error de un campo solo después de que el usuario lo tocó. */
  protected showError(field: keyof typeof this.form.controls): boolean {
    const control = this.form.controls[field];
    return control.invalid && (control.touched || control.dirty);
  }

  protected onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched(); // hace visibles todos los mensajes de error
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
        category_id: value.category_id!, // el validador required garantiza que no es null
      })
      .subscribe({
        next: (task) => {
          this.notifications.success(`Tarea "${task.title}" creada`);
          this.form.reset();
          this.submitting.set(false);
          this.created.emit(task);
        },
        // El interceptor ya mostró el mensaje; aquí solo se libera el botón.
        error: () => this.submitting.set(false),
      });
  }
}
