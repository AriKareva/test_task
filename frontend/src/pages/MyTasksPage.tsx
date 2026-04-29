import { useState } from 'react';
import { useAuthStore } from '../features/auth/store/authStore';
import { fetchUserAssignedTasks } from '../api/tasks';
import KanbanBoard from '../features/tasks/components/KanbanBoard';
import CreateTaskModal from '../features/tasks/components/CreateTaskModal';
import TaskFilters from '../features/tasks/components/TaskFilters';
import TaskHistoryModal from '../features/tasks/components/TaskHistoryModal';  

export default function MyTasksPage() {
  const userId = useAuthStore((s) => s.userId);
  const [showCreate, setShowCreate] = useState(false);
  const [statusFilter, setStatusFilter] = useState('Все');
  const [priorityFilter, setPriorityFilter] = useState('Все');
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);  

  if (!userId) return <div className="loading">Войдите в систему</div>;

  return (
    <div>
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