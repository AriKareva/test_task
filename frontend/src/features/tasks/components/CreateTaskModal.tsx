import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { createTask, fetchUsers } from '../../../api/tasks';
import Modal from '../../../shared/components/Modal';
import { useAuthStore } from '../../../features/auth/store/authStore';

const schema = z.object({
  task_title: z.string().min(1, 'Обязательное поле'),
  description: z.string().optional(),
  deadline: z.string().optional(),
  priority_id: z.number().optional(),
});

type FormData = z.infer<typeof schema>;

interface CreateTaskModalProps {
  onClose: () => void;
}

export default function CreateTaskModal({ onClose }: CreateTaskModalProps) {
  const userId = useAuthStore((s) => s.userId);
  const username = useAuthStore((s) => s.username);

  const [selectedAssigneeId, setSelectedAssigneeId] = useState<number | null>(null);
  const [showUserSelect, setShowUserSelect] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });
  const queryClient = useQueryClient();

  const { data: users } = useQuery({ queryKey: ['users'], queryFn: fetchUsers });

  const mutation = useMutation({
    mutationFn: (data: FormData) =>
      createTask({
        task_title: data.task_title,
        description: data.description || null,
        deadline: data.deadline ? new Date(data.deadline).toISOString() : null,
        priority_id: data.priority_id || null,
        assignee_id: selectedAssigneeId,  
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['myCreatedTasks'] });
      queryClient.invalidateQueries({ queryKey: ['myTasks'] });
      queryClient.invalidateQueries({ queryKey: ['allTasks'] });
      onClose();
    },
    onError: (error: any) => {
      alert(error?.response?.data?.detail || 'Ошибка');
    },
  });

  const onSubmit = (data: FormData) => {
    if (!userId) return;
    mutation.mutate(data);
  };

  return (
    <Modal onClose={onClose}>
      <form className="auth-form" onSubmit={handleSubmit(onSubmit)}>
        <h2>Создать задачу</h2>

        <input {...register('task_title')} placeholder="Название задачи" autoFocus />
        {errors.task_title && <p className="error-message">{errors.task_title.message}</p>}

        <textarea {...register('description')} placeholder="Описание" className="form-textarea" />

        <div className="form-group" style={{ marginBottom: 12 }}>
          <label className="label">Дедлайн</label>
          <input type="datetime-local" {...register('deadline')} className="input" />
        </div>

        <div className="form-group" style={{ marginBottom: 12 }}>
          <label className="label">Приоритет</label>
          <select {...register('priority_id', { valueAsNumber: true })} className="select">
            <option value="">Не выбран</option>
            <option value={1}>Низкий</option>
            <option value={2}>Средний</option>
            <option value={3}>Высокий</option>
            <option value={4}>Критичный</option>
          </select>
        </div>

        <div className="form-group" style={{ marginBottom: 16 }}>
          <label className="label">Исполнитель</label>
          {!showUserSelect ? (
            <div className="assignee-box">
              <span>{users?.find(u => u.user_id === selectedAssigneeId)?.login || username || 'Вы'}</span>
              <button type="button" className="btn btn--secondary" onClick={() => setShowUserSelect(true)}>
                Сменить
              </button>
            </div>
          ) : (
            <select
              value={selectedAssigneeId ?? ''}
              onChange={(e) => {
                const id = Number(e.target.value);
                setSelectedAssigneeId(id || null);
                setShowUserSelect(false);
              }}
              className="select"
            >
              <option value="">Не назначен</option>
              {users?.map(u => (
                <option key={u.user_id} value={u.user_id}>{u.login}</option>
              ))}
            </select>
          )}
        </div>

        <button className="btn btn--primary" type="submit" disabled={mutation.isPending || !userId}>
          {mutation.isPending ? 'Создание...' : 'Создать'}
        </button>
      </form>
    </Modal>
  );
}