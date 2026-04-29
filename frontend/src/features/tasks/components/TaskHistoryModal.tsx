import { useQuery } from '@tanstack/react-query';
import { fetchTaskStatusHistory, fetchTaskPriorityHistory } from '../../../api/tasks';
import Modal from '../../../shared/components/Modal';

interface TaskHistoryModalProps {
  taskId: number;
  onClose: () => void;
}

export default function TaskHistoryModal({ taskId, onClose }: TaskHistoryModalProps) {
  const { data: statusHistory, isLoading: statusLoading } = useQuery({
    queryKey: ['taskStatusHistory', taskId],
    queryFn: () => fetchTaskStatusHistory(taskId),
  });
  const { data: priorityHistory, isLoading: priorityLoading } = useQuery({
    queryKey: ['taskPriorityHistory', taskId],
    queryFn: () => fetchTaskPriorityHistory(taskId),
  });

  const isLoading = statusLoading || priorityLoading;

  return (
    <Modal onClose={onClose}>
      <h2>История задачи #{taskId}</h2>
      {isLoading ? (
        <div className="loading">Загрузка...</div>
      ) : (
        <div>
          <h3>Статусы</h3>
          {statusHistory && statusHistory.length > 0 ? (
            <ul>
              {statusHistory.map(entry => (
                <li key={`${entry.status_id}-${entry.status_dt}`}>
                  <strong>{entry.status_title}</strong> — {new Date(entry.status_dt).toLocaleString('ru-RU')}
                </li>
              ))}
            </ul>
          ) : (
            <p>Нет данных</p>
          )}

          <h3>Приоритеты</h3>
          {priorityHistory && priorityHistory.length > 0 ? (
            <ul>
              {priorityHistory.map(entry => (
                <li key={`${entry.priority_id}-${entry.priority_dt}`}>
                  <strong>{entry.priority_title}</strong> — {new Date(entry.priority_dt).toLocaleString('ru-RU')}
                </li>
              ))}
            </ul>
          ) : (
            <p>Нет данных</p>
          )}
        </div>
      )}
    </Modal>
  );
}