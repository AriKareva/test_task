import { Link } from 'react-router-dom';
import { useAuthStore } from '../../features/auth/store/authStore';
import UserMenu from '../../features/auth/components/UserMenu';

export default function Header() {
  const token = useAuthStore((s) => s.accessToken);
  return (
    <header className="app-header">
      <nav className="app-header__nav">
        <Link to="/tasks">Все задачи</Link>
        {token && <Link to="/my-tasks">Мои задачи</Link>}
        {token && <Link to="/analytics">Аналитика</Link>}
      </nav>
      <div className="app-header__auth">
        {token ? <UserMenu /> : <Link to="/login">Войти</Link>}
      </div>
    </header>
  );
}