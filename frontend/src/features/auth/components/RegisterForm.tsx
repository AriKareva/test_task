import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { registerUser } from '../../../api/auth';
import { useAuthStore } from '../store/authStore';
import { useNavigate } from 'react-router-dom';

const schema = z.object({
  login: z.string().min(1, 'Обязательное поле'),
  password: z.string().min(4, 'Минимум 4 символа'),
  email: z.string().email('Некорректный email'),
});

type FormData = z.infer<typeof schema>;

export default function RegisterForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema)
  });
  const login = useAuthStore((s) => s.login);
  const navigate = useNavigate();

  const onSubmit = async (data: FormData) => {
    try {
      const res = await registerUser(data.login, data.password, data.email);
      login(res.access_token, res.user_id, res.login);
      navigate('/tasks');
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Ошибка регистрации');
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit(onSubmit)}>
      <h1>Регистрация</h1>
      <input {...register('login')} placeholder="Логин" />
      {errors.login && <p className="error-message">{errors.login.message}</p>}
      <input type="password" {...register('password')} placeholder="Пароль" />
      {errors.password && <p className="error-message">{errors.password.message}</p>}
      <input {...register('email')} placeholder="Email" />
      {errors.email && <p className="error-message">{errors.email.message}</p>}
      <button className="btn btn--primary" type="submit" disabled={isSubmitting}>
        Зарегистрироваться
      </button>
    </form>
  );
}