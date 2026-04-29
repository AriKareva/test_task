import { useQuery } from '@tanstack/react-query';
import { fetchStatuses, fetchPriorities } from '../../../api/tasks';

interface TaskFiltersProps {
  statusFilter: string;
  priorityFilter: string;
  onStatusChange: (value: string) => void;
  onPriorityChange: (value: string) => void;
}

export default function TaskFilters({
  statusFilter, priorityFilter,
  onStatusChange, onPriorityChange
}: TaskFiltersProps) {
  const { data: statuses } = useQuery({ queryKey: ['statuses'], queryFn: fetchStatuses });
  const { data: priorities } = useQuery({ queryKey: ['priorities'], queryFn: fetchPriorities });

  return (
    <div className="filters-bar">
      <select value={statusFilter} onChange={e => onStatusChange(e.target.value)}>
        <option value="Все">Все статусы</option>
        {statuses?.map(s => (
          <option key={s.status_id} value={s.status_title}>{s.status_title}</option>
        ))}
      </select>
      <select value={priorityFilter} onChange={e => onPriorityChange(e.target.value)}>
        <option value="Все">Все приоритеты</option>
        {priorities?.map(p => (
          <option key={p.priority_id} value={p.priority_id}>
            {p.priority_title}
          </option>
        ))}
      </select>
    </div>
  );
}