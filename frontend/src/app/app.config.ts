import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';

import { errorInterceptor } from './core/interceptors/error.interceptor';

// aqui se activa HttpClient y se le engancha el interceptor de errores
export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideHttpClient(withInterceptors([errorInterceptor])),
  ],
};
