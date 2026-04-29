import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';
import TaskCard from './TaskCard';
// import { Task } from '../types';
import { fetchStatuses } from '../../../api/tasks';


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


interface KanbanBoardProps {
  queryKey: string;
  queryFn: () => Promise<Task[]>;
  emptyMessage?: string;
  statusFilter?: string;
  priorityFilter?: string;
  onTaskClick?: (taskId: number) => void;
  renderActions?: (task: Task) => React.ReactNode; 
}

export default function KanbanBoard({
  onTaskClick,
  renderActions,
  queryKey, queryFn, emptyMessage,
  statusFilter = 'Все', priorityFilter = 'Все'
}: KanbanBoardProps) {
  const queryClient = useQueryClient();
  const { data: tasks, isLoading, error } = useQuery({
    queryKey: [queryKey],
    queryFn,
  });

  const { data: statuses } = useQuery({ queryKey: ['statuses'], queryFn: fetchStatuses });

  const [localTasks, setLocalTasks] = useState<Task[]>([]);
  if (tasks && tasks !== localTasks) setLocalTasks(tasks);

  const handleDragStart = (e: React.DragEvent, taskId: number) => {
    e.dataTransfer.setData('text/plain', taskId.toString());
  };

  const handleDrop = (e: React.DragEvent, newStatusTitle: string) => {
    e.preventDefault();
    const taskId = Number(e.dataTransfer.getData('text/plain'));
    if (!taskId) return;
    const task = localTasks.find(t => t.task_id === taskId);
    if (!task) return;
    const oldStatusTitle = task.current_status?.status_title ?? 'Без статуса';
    if (oldStatusTitle === newStatusTitle) return;
    const newStatus = statuses?.find(s => s.status_title === newStatusTitle);
    if (!newStatus) return;

    const updatedTasks = localTasks.map(t =>
      t.task_id === taskId
        ? {
            ...t,
            current_status: {
              status_id: newStatus.status_id,
              status_title: newStatus.status_title,
              status_dt: new Date().toISOString(),
            },
          }
        : t
    );
    setLocalTasks(updatedTasks);
    queryClient.setQueryData([queryKey], updatedTasks);
    updateTaskStatus(taskId, newStatus.status_id); 
  };

  if (isLoading) return <div className="loading">Загрузка...</div>;
  if (error || !statuses) return <div className="loading">Ошибка загрузки данных</div>;

  let filteredTasks = localTasks;
  if (statusFilter !== 'Все')
    filteredTasks = filteredTasks.filter(t => (t.current_status?.status_title ?? 'Без статуса') === statusFilter);
  if (priorityFilter !== 'Все')
    filteredTasks = filteredTasks.filter(
      t => String(t.priority_id ?? '') === String(priorityFilter)
    );
  const columns = statuses.map(status => ({
    statusTitle: status.status_title,
    tasks: filteredTasks.filter(t => (t.current_status?.status_title ?? 'Без статуса') === status.status_title),
  }));
  return (
    <div className="kanban-board">
      {columns.map(col => (
        <div
          key={col.statusTitle}
          className="kanban-column"
          onDragOver={e => e.preventDefault()}
          onDrop={e => handleDrop(e, col.statusTitle)}
        >
          <h3 className="kanban-column__title">{col.statusTitle}</h3>
          <div className="kanban-column__list">
            {col.tasks.length === 0 && (
              <p className="text-center" style={{ color: '#94a3b8' }}>
                {emptyMessage || 'Нет задач'}
              </p>
            )}
            {col.tasks.map(task => (
              <TaskCard
                key={task.task_id}
                task={task}
                onDragStart={handleDragStart}
                onClick={onTaskClick}
              >
                {/* Пробрасываем доп. действия */}
                {renderActions?.(task)}
              </TaskCard>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}