import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';

import { NotificationService } from '../services/notification.service';

// todas las respuestas pasan por aqui, si alguna falla se muestra el aviso rojo
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  // inject tiene que ir aqui arriba, dentro del catchError ya no funciona
  const notifications = inject(NotificationService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      notifications.error(toFriendlyMessage(error));
      // se vuelve a lanzar para que el componente tambien se entere (ej. para quitar el "Guardando...")
      return throwError(() => error);
    }),
  );
};

function toFriendlyMessage(error: HttpErrorResponse): string {
  // status 0 es que ni siquiera hubo respuesta: backend apagado, sin red o cors
  if (error.status === 0) {
    return 'No se pudo conectar con el servidor. Verifica que el backend esté en ejecución.';
  }

  const detail = error.error?.detail;
  // nuestros errores llegan como {"detail": "texto"}
  if (typeof detail === 'string') {
    return detail;
  }
  // los de pydantic llegan como una lista, de cada uno se saca el nombre del campo
  if (Array.isArray(detail)) {
    const fields = detail.map((d: { loc: string[] }) => d.loc.at(-1)).join(', ');
    return `Datos inválidos en: ${fields}`;
  }
  return 'Ocurrió un error inesperado. Inténtalo nuevamente.';
}
