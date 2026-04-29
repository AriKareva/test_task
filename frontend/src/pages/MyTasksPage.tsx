import { useState } from 'react';
import { useAuthStore } from '../features/auth/store/authStore';
import { fetchUserAssignedTasks, updateTaskStatus, fetchStatuses } from '../api/tasks';
import KanbanBoard from '../features/tasks/components/KanbanBoard';
import CreateTaskModal from '../features/tasks/components/CreateTaskModal';
import TaskFilters from '../features/tasks/components/TaskFilters';
import TaskHistoryModal from '../features/tasks/components/TaskHistoryModal';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

export default function MyTasksPage() {
  const userId = useAuthStore((s) => s.userId);
  const [showCreate, setShowCreate] = useState(false);
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);
  const [statusFilter, setStatusFilter] = useState('Все');
  const [priorityFilter, setPriorityFilter] = useState('Все');

  const queryClient = useQueryClient();

  const { data: statuses } = useQuery({ queryKey: ['statuses'], queryFn: fetchStatuses });

  const statusMutation = useMutation({
    mutationFn: ({ taskId, statusId }: { taskId: number; statusId: number }) =>
      updateTaskStatus(taskId, statusId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['myTasks'] });
    },
  });

  if (!userId) return <div className="loading">Войдите в систему</div>;

  const renderActions = (task: Task) => (
    <div className="task-card__actions">
      <select
        className="select"
        value={task.current_status?.status_id ?? ''}
        onChange={(e) => {
          const newStatusId = Number(e.target.value);
          if (newStatusId && newStatusId !== task.current_status?.status_id) {
            statusMutation.mutate({ taskId: task.task_id, statusId: newStatusId });
          }
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <option value="">Сменить статус</option>
        {statuses?.map(s => (
          <option key={s.status_id} value={s.status_id}>{s.status_title}</option>
        ))}
      </select>
    </div>
  );

  return (
    <div>
      <button className="btn btn--primary" onClick={() => setShowCreate(true)} style={{ marginBottom: 16 }}>
        + Новая задача
      </button>
      <TaskFilters
        statusFilter={statusFilter}
        priorityFilter={priorityFilter}
        onStatusChange={setStatusFilter}
        onPriorityChange={setPriorityFilter}
      />
      <KanbanBoard
        queryKey="myTasks"
        queryFn={() => fetchUserAssignedTasks(userId)}
        emptyMessage="У вас пока нет задач"
        statusFilter={statusFilter}
        priorityFilter={priorityFilter}
        renderActions={renderActions}
        onTaskClick={setSelectedTaskId}
      />
      {showCreate && <CreateTaskModal onClose={() => setShowCreate(false)} />}
      {selectedTaskId && (
        <TaskHistoryModal
          taskId={selectedTaskId}
          onClose={() => setSelectedTaskId(null)}
        />
      )}
    </div>
  );
}