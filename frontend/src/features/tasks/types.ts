// export interface Task {
//   task_id: number | null;
//   task_title: string | null;
//   description: string | null;
//   author_id: number | null;
//   // current_status: string ;
//   assignee_id: number | null;
// }

export interface Task {
  description?: string | null;
  priority?: number | null;
  assignee_id?: number | null;
  author_id?: number | null;
  task_id?: number | null;
  task_title?: string | null;
}