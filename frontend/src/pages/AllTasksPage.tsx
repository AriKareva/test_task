import { useState } from 'react';
import { fetchAllTasks } from '../api/tasks';
import KanbanBoard from '../features/tasks/components/KanbanBoard';
import TaskFilters from '../features/tasks/components/TaskFilters';
import TaskHistoryModal from '../features/tasks/components/TaskHistoryModal';   

export default function AllTasksPage() {
  const [statusFilter, setStatusFilter] = useState('Все');
  const [priorityFilter, setPriorityFilter] = useState('Все');
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null); 

  return (
    <div>
      <TaskFilters
        statusFilter={statusFilter}
        priorityFilter={priorityFilter}
        onStatusChange={setStatusFilter}
        onPriorityChange={setPriorityFilter}
      />
      <KanbanBoard
        queryKey="allTasks"
        queryFn={fetchAllTasks}
        emptyMessage="Нет задач"
        statusFilter={statusFilter}
        priorityFilter={priorityFilter}
        onTaskClick={setSelectedTaskId} 
      />
      {selectedTaskId && (
        <TaskHistoryModal
          taskId={selectedTaskId}
          onClose={() => setSelectedTaskId(null)}
        />
      )}
    </div>
  );
}