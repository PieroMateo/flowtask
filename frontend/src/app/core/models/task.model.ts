import { Category } from './category.model';

// tienen que coincidir con el enum TaskStatus del backend (enums.py)
export const TASK_STATUSES = ['Pendiente', 'En Progreso', 'Completada'] as const;

// sale del arreglo de arriba, queda como 'Pendiente' | 'En Progreso' | 'Completada'
export type TaskStatus = (typeof TASK_STATUSES)[number];

// lo que devuelve la API (TaskRead)
export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  due_date: string; // llega como "2026-10-30"
  category_id: number;
  category: Category;
}

// lo que se manda en el POST (TaskCreate)
export interface TaskCreate {
  title: string;
  description?: string | null;
  status?: TaskStatus;
  due_date: string;
  category_id: number;
}

// para el PATCH, Partial vuelve opcionales todos los campos
export type TaskUpdate = Partial<TaskCreate>;

// si un filtro queda en undefined es que no se filtra por ese campo
export interface TaskFilters {
  status?: TaskStatus;
  categoryId?: number;
}
