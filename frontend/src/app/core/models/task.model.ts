import { Category } from './category.model';

/** Valores permitidos, en el mismo orden que el Enum TaskStatus del backend. */
export const TASK_STATUSES = ['Pendiente', 'En Progreso', 'Completada'] as const;

/** 'Pendiente' | 'En Progreso' | 'Completada', derivado del arreglo de arriba. */
export type TaskStatus = (typeof TASK_STATUSES)[number];

/** Espejo de TaskRead: lo que devuelve la API. */
export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  /** Fecha ISO sin hora, ej. "2026-10-30". */
  due_date: string;
  category_id: number;
  category: Category;
}

/** Espejo de TaskCreate: body de POST /tasks. */
export interface TaskCreate {
  title: string;
  description?: string | null;
  status?: TaskStatus;
  due_date: string;
  category_id: number;
}

/** Espejo de TaskUpdate: body de PATCH /tasks/{id}. Todo es opcional. */
export type TaskUpdate = Partial<TaskCreate>;

/** Filtros del tablero. undefined = sin filtrar por ese campo. */
export interface TaskFilters {
  status?: TaskStatus;
  categoryId?: number;
}
