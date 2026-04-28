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
      <button className="btn btn--primary" onClick={() => setShowCreate(true)}>
        + Новая задача
      </button>
      <KanbanBoard
        queryKey="myTasks"
        queryFn={() => fetchUserAssignedTasks(userId)}
        emptyMessage="У вас пока нет задач"
      />
      {showCreate && <CreateTaskModal onClose={() => setShowCreate(false)} />}
    </div>
  );
}