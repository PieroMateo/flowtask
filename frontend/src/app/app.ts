import { Component } from '@angular/core';

import { TaskBoard } from './features/tasks/task-board/task-board';
import { Notifications } from './shared/notifications/notifications';

@Component({
  selector: 'app-root',
  imports: [TaskBoard, Notifications],
  templateUrl: './app.html',
})
export class App {}
