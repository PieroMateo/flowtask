import { Component, input, output } from '@angular/core';

import { Category } from '../../../core/models/category.model';
import { TASK_STATUSES, TaskFilters, TaskStatus } from '../../../core/models/task.model';

/** Presentacional: muestra los filtros actuales y emite los nuevos cuando el usuario cambia algo. */
@Component({
  selector: 'app-filter-bar',
  templateUrl: './filter-bar.html',
})
export class FilterBar {
  readonly filters = input.required<TaskFilters>();
  readonly categories = input<Category[]>([]);

  readonly filtersChange = output<TaskFilters>();

  protected readonly statuses = TASK_STATUSES;

  protected onStatusChange(value: string): void {
    // "" es la opción "Todos": se traduce a undefined (= sin filtro).
    const status = value ? (value as TaskStatus) : undefined;
    this.filtersChange.emit({ ...this.filters(), status });
  }

  protected onCategoryChange(value: string): void {
    const categoryId = value ? Number(value) : undefined;
    this.filtersChange.emit({ ...this.filters(), categoryId });
  }
}
