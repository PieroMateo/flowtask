import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';

import { errorInterceptor } from './core/interceptors/error.interceptor';

// Herramientas globales de la app: aquí se "enchufa" HttpClient con su interceptor.
export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideHttpClient(withInterceptors([errorInterceptor])),
  ],
};
