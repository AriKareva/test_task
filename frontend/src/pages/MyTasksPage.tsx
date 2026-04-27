import { useState } from 'react';
import { useAuthStore } from '../features/auth/store/authStore';
import { fetchMyTasks, updateTaskStatus } from '../api/tasks';
import KanbanBoard from '../features/tasks/components/KanbanBoard';
import CreateTaskModal from '../features/tasks/components/CreateTaskModal';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Task } from '../features/tasks/types';

export default function MyTasksPage() {
  const userId = useAuthStore((s) => s.userId);
  const [showCreate, setShowCreate] = useState(false);
  const queryClient = useQueryClient();

  const statusMutation = useMutation({
    mutationFn: ({ taskId, statusId }: { taskId: number; statusId: number }) =>
      updateTaskStatus(taskId, statusId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['myTasks'] });
    },
  });

  if (!userId) return <div className="loading">Войдите в систему</div>;

  const renderActions = (task: Task) => (
    <select
      value={task.current_status}
      onChange={(e) => {
        const statusMap: Record<string, number> = {
          'Создана': 1,
          'В работе': 2,
          'Выполнена': 3,
        };
        const newStatusId = statusMap[e.target.value];
        if (newStatusId) {
          statusMutation.mutate({ taskId: task.task_id, statusId: newStatusId });
        }
      }}
      style={{ marginTop: 4 }}
    >
      <option value="">Изменить статус</option>
      <option value="Создана">Создана</option>
      <option value="В работе">В работе</option>
      <option value="Выполнена">Выполнена</option>
    </select>
  );

  return (
    <div>
      <button className="btn btn--primary" onClick={() => setShowCreate(true)}>
        + Новая задача
      </button>
      <KanbanBoard
        queryKey="myTasks"
        queryFn={() => fetchMyTasks(userId)}
        emptyMessage="У вас пока нет задач"
        renderActions={renderActions}
      />
      {showCreate && <CreateTaskModal onClose={() => setShowCreate(false)} />}
    </div>
  );
}