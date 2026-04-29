import { memo, ReactNode } from 'react';


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

interface TaskCardProps {
  task: Task;
  onDragStart?: (e: React.DragEvent, taskId: number) => void;
  onClick?: (taskId: number) => void;
  children?: ReactNode; 
}

const TaskCard = memo(function TaskCard({ task, onDragStart, onClick, children }: TaskCardProps) {
  const authorName = task.author_login ?? `Автор #${task.author_id}`;
  const assigneeName = task.cur_assignee?.assignee_login ?? 'Нет';
  const deadline = task.deadline
    ? new Date(task.deadline).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    : null;

  const handleClick = () => {
    if (onClick) onClick(task.task_id);
  };

  return (
    <div
      className="task-card"
      draggable
      onDragStart={e => onDragStart?.(e, task.task_id)}
      onClick={handleClick}
      style={{ cursor: onClick ? 'pointer' : 'default' }}
    >
      <div className="task-card__title">{task.task_title}</div>
      {task.description && (
        <div className="task-card__description">{task.description}</div>
      )}
      <div className="task-card__meta">
        <span>Автор: {authorName}</span>
        <span>Исполнитель: {assigneeName}</span>
      </div>
      {deadline && (
        <div className="task-card__deadline">Дедлайн: {deadline}</div>
      )}
      <div className="task-card__status">
        Статус: {task.current_status?.status_title ?? 'Не задан'}
      </div>
      {children && <div className="task-card__actions">{children}</div>}
    </div>
  );
});

export default TaskCard;