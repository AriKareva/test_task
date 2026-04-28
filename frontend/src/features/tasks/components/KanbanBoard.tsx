import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';
import TaskCard from './TaskCard';
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

interface KanbanBoardProps {
  queryKey: string;
  queryFn: () => Promise<Task[]>;
  emptyMessage?: string;
}

const STATUSES = ['Создана', 'В работе', 'Выполнена'];

export default function KanbanBoard({ queryKey, queryFn, emptyMessage }: KanbanBoardProps) {
  const queryClient = useQueryClient();
  const { data: tasks, isLoading, error } = useQuery({
    queryKey: [queryKey],
    queryFn,
  });

  // Локальное состояние колонок (для мгновенного отклика)
  const [localTasks, setLocalTasks] = useState<Task[]>([]);

  // Синхронизируем локальное состояние с данными с сервера
  if (tasks && tasks !== localTasks) {
    setLocalTasks(tasks);
  }

  const handleDragStart = (e: React.DragEvent, taskId: number) => {
    e.dataTransfer.setData('text/plain', taskId.toString());
  };

  const handleDrop = (e: React.DragEvent, newStatus: string) => {
    e.preventDefault();
    const taskId = Number(e.dataTransfer.getData('text/plain'));
    if (!taskId) return;

    // Находим задачу и её старый статус
    const task = localTasks.find((t) => t.task_id === taskId);
    if (!task) return;

    const oldStatus = task.current_status || 'Создана';
    if (oldStatus === newStatus) return;

    // Обновляем локальное состояние (оптимистично)
    const updatedTasks = localTasks.map((t) =>
      t.task_id === taskId ? { ...t, current_status: newStatus } : t
    );
    setLocalTasks(updatedTasks);

    // Оптимистично обновляем кэш React Query
    queryClient.setQueryData([queryKey], updatedTasks);

    // Здесь позже можно отправить PATCH-запрос на бэкенд для сохранения статуса
    // Например: updateTaskStatus(taskId, newStatusId);
  };

  if (isLoading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="loading">Ошибка загрузки задач</div>;

  const columns = STATUSES.map((status) => ({
    status,
    tasks: localTasks.filter((t) => (t.current_status || 'Создана') === status),
  }));

  return (
    <div className="kanban-board">
      {columns.map((col) => (
        <div
          key={col.status}
          className="kanban-column"
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => handleDrop(e, col.status)}
        >
          <h3 className="kanban-column__title">{col.status}</h3>
          <div className="kanban-column__list">
            {col.tasks.length === 0 && (
              <p className="text-center" style={{ color: '#94a3b8' }}>
                {emptyMessage || 'Нет задач'}
              </p>
            )}
            {col.tasks.map((task) => (
              <TaskCard key={task.task_id} task={task} onDragStart={handleDragStart} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}