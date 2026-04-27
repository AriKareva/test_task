import KanbanBoard from '../features/tasks/components/KanbanBoard';
import { fetchAllTasks } from '../api/tasks';

export default function AllTasksPage() {
  return <KanbanBoard queryKey="allTasks" queryFn={fetchAllTasks} />;
}