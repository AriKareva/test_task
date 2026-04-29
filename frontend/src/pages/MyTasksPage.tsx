import { useState } from 'react';
import { useAuthStore } from '../features/auth/store/authStore';
import { fetchUserAssignedTasks } from '../api/tasks';
import KanbanBoard from '../features/tasks/components/KanbanBoard';
import CreateTaskModal from '../features/tasks/components/CreateTaskModal';


export default function MyTasksPage() {
  const userId = useAuthStore((s) => s.userId);
  const [showCreate, setShowCreate] = useState(false);

  if (!userId) return <div className="loading">Войдите в систему</div>;

  return (
    <div>
      <KanbanBoard
        queryKey="myTasks"
        queryFn={() => fetchUserAssignedTasks(userId)}
        emptyMessage="Нет задач"
      />
      {showCreate && <CreateTaskModal onClose={() => setShowCreate(false)} />}
    </div>
  );
}