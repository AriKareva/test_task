import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createTask } from '../../../api/tasks';
import Modal from '../../../shared/components/Modal';

const schema = z.object({
  task_title: z.string().min(1, 'Обязательное поле'),
  description: z.string().optional(),
});

type FormData = z.infer<typeof schema>;

interface CreateTaskModalProps {
  onClose: () => void;
}

export default function CreateTaskModal({ onClose }: CreateTaskModalProps) {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema)
  });
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['myTasks'] });
      queryClient.invalidateQueries({ queryKey: ['allTasks'] });
      onClose();
    },
  });

  const onSubmit = (data: FormData) => mutation.mutate(data);

  return (
    <Modal onClose={onClose}>
      <form className="auth-form" onSubmit={handleSubmit(onSubmit)}>
        <h2>Создать задачу</h2>
        <input {...register('task_title')} placeholder="Название задачи" />
        {errors.task_title && <p className="error-message">{errors.task_title.message}</p>}
        <textarea {...register('description')} placeholder="Описание (необязательно)" rows={3} style={{ width: '100%', marginBottom: 12 }} />
        <button className="btn btn--primary" type="submit" disabled={mutation.isPending}>
          Создать
        </button>
      </form>
    </Modal>
  );
}