import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';

import { NotificationService } from '../services/notification.service';

/** Revisa TODAS las respuestas HTTP y muestra un aviso amigable cuando algo falla. */
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  // inject() solo funciona aquí arriba (contexto de inyección), no dentro del catchError.
  const notifications = inject(NotificationService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      notifications.error(toFriendlyMessage(error));
      // Se relanza el error para que el componente también pueda reaccionar (ej. quitar el loading).
      return throwError(() => error);
    }),
  );
};

function toFriendlyMessage(error: HttpErrorResponse): string {
  // status 0: la petición ni siquiera obtuvo respuesta (backend apagado, sin red o CORS).
  if (error.status === 0) {
    return 'No se pudo conectar con el servidor. Verifica que el backend esté en ejecución.';
  }

  const detail = error.error?.detail;
  // Nuestros errores de dominio llegan como {"detail": "texto"}.
  if (typeof detail === 'string') {
    return detail;
  }
  // Los errores de validación de Pydantic llegan como {"detail": [{loc, msg}, ...]}.
  if (Array.isArray(detail)) {
    const fields = detail.map((d: { loc: string[] }) => d.loc.at(-1)).join(', ');
    return `Datos inválidos en: ${fields}`;
  }
  return 'Ocurrió un error inesperado. Inténtalo nuevamente.';
}
