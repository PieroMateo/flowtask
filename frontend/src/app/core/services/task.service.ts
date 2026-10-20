import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Task, TaskCreate, TaskFilters, TaskStatus, TaskUpdate } from '../models/task.model';

/** Único lugar del frontend que sabe cómo hablar con /tasks. */
@Injectable({ providedIn: 'root' })
export class TaskService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = `${environment.apiUrl}/tasks`;

  getAll(filters: TaskFilters = {}): Observable<Task[]> {
    // HttpParams es inmutable: cada set() devuelve una copia nueva.
    let params = new HttpParams();
    if (filters.status) params = params.set('status', filters.status);
    if (filters.categoryId) params = params.set('category_id', filters.categoryId);
    return this.http.get<Task[]>(this.apiUrl, { params });
  }

  create(data: TaskCreate): Observable<Task> {
    return this.http.post<Task>(this.apiUrl, data);
  }

  update(id: number, changes: TaskUpdate): Observable<Task> {
    return this.http.patch<Task>(`${this.apiUrl}/${id}`, changes);
  }

  updateStatus(id: number, status: TaskStatus): Observable<Task> {
    return this.update(id, { status });
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
