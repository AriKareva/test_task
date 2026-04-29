import { useState } from 'react';
import { useAuthStore } from '../features/auth/store/authStore';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  fetchUserCreatedTasks,
  updateTaskAssignee,
  updateTaskPriority,
  deleteTask,
  fetchUsers,
  fetchPriorities,
} from '../api/tasks';
import KanbanBoard from '../features/tasks/components/KanbanBoard';
import TaskFilters from '../features/tasks/components/TaskFilters';
import CreateTaskModal from '../features/tasks/components/CreateTaskModal';
import TaskHistoryModal from '../features/tasks/components/TaskHistoryModal';

export default function MyCreatedTasksPage() {
  const userId = useAuthStore((s) => s.userId);
  const [showCreate, setShowCreate] = useState(false);
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);
  const [statusFilter, setStatusFilter] = useState('Все');
  const [priorityFilter, setPriorityFilter] = useState('Все');

  const queryClient = useQueryClient();

  // Загрузка пользователей и приоритетов для выпадающих списков
  const { data: users } = useQuery({ queryKey: ['users'], queryFn: fetchUsers });
  const { data: priorities } = useQuery({ queryKey: ['priorities'], queryFn: fetchPriorities });

  // Мутации
  const deleteMutation = useMutation({
    mutationFn: deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['myCreatedTasks'] });
    },
  });

  const assigneeMutation = useMutation({
    mutationFn: ({ taskId, assigneeId }: { taskId: number; assigneeId: number }) =>
      updateTaskAssignee(taskId, assigneeId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['myCreatedTasks'] });
    },
  });

  const priorityMutation = useMutation({
    mutationFn: ({ taskId, priorityId }: { taskId: number; priorityId: number }) =>
      updateTaskPriority(taskId, priorityId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['myCreatedTasks'] });
    },
  });

  if (!userId) return <div className="loading">Войдите в систему</div>;

  const renderActions = (task: Task) => (
    <div className="task-card__actions">
      {/* Смена исполнителя */}
      <select
        value={task.cur_assignee?.assignee_id ?? ''}
        onChange={(e) => {
          const newId = Number(e.target.value);
          if (newId && newId !== task.cur_assignee?.assignee_id) {
            assigneeMutation.mutate({ taskId: task.task_id, assigneeId: newId });
          }
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <option value="">Не назначен</option>
        {users?.map(u => (
          <option key={u.user_id} value={u.user_id}>{u.login}</option>
        ))}
      </select>

      {/* Смена приоритета */}
      <select
        value={task.priority ?? ''}
        onChange={(e) => {
          const newPriority = Number(e.target.value);
          if (newPriority) {
            priorityMutation.mutate({ taskId: task.task_id, priorityId: newPriority });
          }
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <option value="">Без приоритета</option>
        {priorities?.map(p => (
          <option key={p.priority_id} value={p.priority_id}>{p.priority_title}</option>
        ))}
      </select>

      {/* Удаление */}
      <button
        className="btn btn--danger"
        onClick={(e) => {
          e.stopPropagation();
          if (confirm('Удалить задачу?')) {
            deleteMutation.mutate(task.task_id);
          }
        }}
      >
        Удалить
      </button>
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
        queryKey="myCreatedTasks"
        queryFn={() => fetchUserCreatedTasks(userId!)}
        emptyMessage="У вас пока нет созданных задач"
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