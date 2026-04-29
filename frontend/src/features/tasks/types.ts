export interface TaskAssignee {
  assignee_id: number;
  assignee_login: string;
  assignee_dt: string;
}

export interface TaskStatus {
  status_id: number;
  status_title: string;
  status_dt: string;
}

export interface Task {
  task_id: number;
  task_title: string;
  description: string | null;
  author_id: number;
  author_login?: string | null;
  cur_assignee: TaskAssignee | null;
  current_status: TaskStatus | null;
  priority?: string | null;
  deadline?: string | null;
}