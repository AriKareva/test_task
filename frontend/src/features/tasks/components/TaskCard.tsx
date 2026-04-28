import { memo } from 'react';
// import { Task } from '../types';

export interface Task {
  task_id: number;
  task_title: string;
  description: string | null;
  author_id: number;
  assignee_id: number | null;
  priority: number | null;
  current_status?: string; 
}

interface TaskCardProps {
  task: Task;
}

const TaskCard = memo(function TaskCard({ task }: TaskCardProps) {
  return (
    <div className="task-card">
      <div className="task-card__title">{task.task_title}</div>
      {task.description && <div className="task-card__description">{task.description}</div>}
      <div className="task-card__meta">
        <span>Автор: {task.author_id}</span>
        {task.assignee_id && <span>Исполнитель: {task.assignee_id}</span>}
      </div>
    </div>
  );
});

export default TaskCard;