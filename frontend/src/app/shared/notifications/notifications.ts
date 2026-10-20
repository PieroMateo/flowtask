import { Component, inject } from '@angular/core';

import { NotificationService } from '../../core/services/notification.service';

@Component({
  selector: 'app-notifications',
  templateUrl: './notifications.html',
})
export class Notifications {
  protected readonly notificationService = inject(NotificationService);
}
