import { Component, input, output } from '@angular/core';

import { Category } from '../../../core/models/category.model';
import { TASK_STATUSES, TaskFilters, TaskStatus } from '../../../core/models/task.model';

// muestra los filtros actuales y emite los nuevos, quien llama al backend es el board
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
    // la opcion "Todos" viene vacia, eso se pasa como undefined para no filtrar
    const status = value ? (value as TaskStatus) : undefined;
    // se copian los filtros que ya habia para no perder la categoria elegida
    this.filtersChange.emit({ ...this.filters(), status });
  }

  protected onCategoryChange(value: string): void {
    const categoryId = value ? Number(value) : undefined;
    this.filtersChange.emit({ ...this.filters(), categoryId });
  }
}
