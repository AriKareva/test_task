import { memo, ReactNode } from 'react';
import { Task } from '../../tasks/types';

interface TaskCardProps {
  task: Task;
  children?: ReactNode;
}

const TaskCard = memo(function TaskCard({ task, children }: TaskCardProps) {
  return (
    <div className="task-card">
      <div className="task-card__title">{task.task_title}</div>
      {task.description && <div className="task-card__description">{task.description}</div>}
      <div className="task-card__meta">
        <span>Автор: {task.author_id}</span>
        {task.assignee_id && <span>Исполнитель: {task.assignee_id}</span>}
      </div>
      {children && <div className="task-card__actions">{children}</div>}
    </div>
  );
});

export default TaskCard;