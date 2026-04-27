import RegisterForm from '../features/auth/components/RegisterForm';
import { Link } from 'react-router-dom';

export default function RegisterPage() {
  return (
    <div>
      <RegisterForm />
      <p className="text-center mt-16">
        Уже есть аккаунт? <Link to="/login" style={{ color: '#6366f1' }}>Войти</Link>
      </p>
    </div>
  );
}