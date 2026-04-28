import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createTask } from '../../../api/tasks';
import Modal from '../../../shared/components/Modal';
import { useAuthStore } from '../../../features/auth/store/authStore';

const schema = z.object({
  task_title: z.string().min(1, 'Обязательное поле'),
  description: z.string().optional(),
  priority_id: z.number().optional(),
});

type FormData = z.infer<typeof schema>;

interface CreateTaskModalProps {
  onClose: () => void;
}

export default function CreateTaskModal({ onClose }: CreateTaskModalProps) {
  const userId = useAuthStore((s) => s.userId);
  const username = useAuthStore((s) => s.username);

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (data: FormData) =>
      createTask({
        task_title: data.task_title,
        description: data.description || null,
        priority_id: data.priority_id || null,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['myTasks'] });
      queryClient.invalidateQueries({ queryKey: ['allTasks'] });
      onClose();
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

        <input
          {...register('task_title')}
          placeholder="Название задачи"
          autoFocus
        />
        {errors.task_title && <p className="error-message">{errors.task_title.message}</p>}

        <textarea
          {...register('description')}
          placeholder="Описание (необязательно)"
          className="form-textarea"
        />

        <div className="form-group" style={{ marginBottom: 12 }}>
          <label style={{ display: 'block', marginBottom: 4, fontSize: 14, color: '#475569' }}>
            Приоритет
          </label>
          <select
            {...register('priority_id', { valueAsNumber: true })}
            style={{ width: '100%', padding: '10px 12px', borderRadius: 6, border: '1px solid #cbd5e1' }}
          >
            <option value="">Не выбран</option>
            <option value="1">Низкий</option>
            <option value="2">Средний</option>
            <option value="3">Высокий</option>
            <option value="4">Критичный</option>
          </select>
        </div>

        <div className="form-group" style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 4, fontSize: 14, color: '#475569' }}>
            Исполнитель
          </label>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ flex: 1, padding: '10px 12px', background: '#f1f5f9', borderRadius: 6 }}>
              {username || 'Вы'}
            </span>
            <button
              type="button"
              className="btn btn--secondary"
              onClick={() => alert('Смена исполнителя будет доступна позже')}
            >
              Сменить
            </button>
          </div>
          <input type="hidden" value={userId || ''} />
        </div>

        <button
          className="btn btn--primary"
          type="submit"
          disabled={mutation.isPending || !userId}
        >
          {mutation.isPending ? 'Создание...' : 'Создать'}
        </button>
      </form>
    </Modal>
  );
}