import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useAuthStore } from '../store/authStore';
import { loginUser } from '../../../api/auth';
import { useNavigate } from 'react-router-dom';

const schema = z.object({
  login: z.string().min(1, 'Обязательное поле'),
  password: z.string().min(4, 'Минимум 4 символа'),
});

type FormData = z.infer<typeof schema>;

export default function LoginForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema)
  });
  const login = useAuthStore((s) => s.login);
  const navigate = useNavigate();

  const onSubmit = async (data: FormData) => {
    try {
      const res = await loginUser(data.login, data.password);
      login(res.access_token, res.user_id, res.login);
      navigate('/tasks');
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Неверные учётные данные');
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit(onSubmit)}>
      <h1>Вход</h1>
      <input {...register('login')} placeholder="Логин" />
      {errors.login && <p className="error-message">{errors.login.message}</p>}
      <input type="password" {...register('password')} placeholder="Пароль" />
      {errors.password && <p className="error-message">{errors.password.message}</p>}
      <button className="btn btn--primary" type="submit" disabled={isSubmitting}>
        Войти
      </button>
    </form>
  );
}