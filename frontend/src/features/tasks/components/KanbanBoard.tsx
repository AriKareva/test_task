import { useQuery } from '@tanstack/react-query';
import TaskCard from './TaskCard';
import { Task } from '../types';

interface KanbanBoardProps {
  queryKey: string;
  queryFn: () => Promise<Task[]>;
  emptyMessage?: string;
  renderActions?: (task: Task) => React.ReactNode;
}

const STATUSES = ['Создана', 'В работе', 'Выполнена'];

export default function KanbanBoard({ queryKey, queryFn, emptyMessage, renderActions }: KanbanBoardProps) {
  const { data: tasks, isLoading, error } = useQuery({ queryKey: [queryKey], queryFn });

  if (isLoading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="loading">Ошибка загрузки задач</div>;

  const columns = STATUSES.map(status => ({
    status,
    tasks: tasks?.filter(t => t.current_status === status) || [],
  }));

  return (
    <div className="kanban-board">
      {columns.map(col => (
        <div key={col.status} className="kanban-column">
          <h3 className="kanban-column__title">{col.status}</h3>
          <div className="kanban-column__list">
            {col.tasks.length === 0 && <p className="text-center" style={{ color: '#94a3b8' }}>{emptyMessage || 'Нет задач'}</p>}
            {col.tasks.map(task => (
              <TaskCard key={task.task_id} task={task}>
                {renderActions?.(task)}
              </TaskCard>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}