import { useState } from 'react';
import { fetchAllTasks } from '../api/tasks';
import KanbanBoard from '../features/tasks/components/KanbanBoard';
import CreateTaskModal from '../features/tasks/components/CreateTaskModal';


export default function MyTasksPage() {
  const [showCreate, setShowCreate] = useState(false);

  return (
    <div>
      <button className="btn btn--primary" onClick={() => setShowCreate(true)}>
        + Новая задача
      </button>
      <KanbanBoard
        queryKey="allTasks"
        queryFn={fetchAllTasks} 
        emptyMessage="Нет задач"
      />
      {showCreate && <CreateTaskModal onClose={() => setShowCreate(false)} />}
    </div>
  );
}