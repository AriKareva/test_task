import LoginForm from '../features/auth/components/LoginForm';
import { Link } from 'react-router-dom';

export default function LoginPage() {
  return (
    <div>
      <LoginForm />
      <p className="text-center mt-16">
        Нет аккаунта? <Link to="/register" style={{ color: '#6366f1' }}>Зарегистрироваться</Link>
      </p>
    </div>
  );
}