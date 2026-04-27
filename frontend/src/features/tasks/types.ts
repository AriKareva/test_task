export interface Task {
  task_id: number;
  task_title: string;
  description: string | null;
  author_id: number;
  current_status: string;
  assignee_id: number | null;
}