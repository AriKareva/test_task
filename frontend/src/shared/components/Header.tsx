import { Link, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../features/auth/store/authStore';
import UserMenu from '../../features/auth/components/UserMenu';

export default function Header() {
  const token = useAuthStore((s) => s.accessToken);
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="app-header">
      <nav className="app-header__nav">
        <Link
          to="/tasks"
          className={isActive('/tasks') ? 'active' : ''}
          aria-current={isActive('/tasks') ? 'page' : undefined}
        >
          Все задачи
        </Link>
        {token && (
          <Link
            to="/my-tasks"
            className={isActive('/my-tasks') ? 'active' : ''}
            aria-current={isActive('/my-tasks') ? 'page' : undefined}
          >
            Мои задачи
          </Link>
        )}
        <Link
              to="/my-created-tasks"
              className={isActive('/my-created-tasks') ? 'active' : ''}
              aria-current={isActive('/my-created-tasks') ? 'page' : undefined}
            >
              Мои созданные
        </Link>
        {token && (
          <Link
            to="/analytics"
            className={isActive('/analytics') ? 'active' : ''}
            aria-current={isActive('/analytics') ? 'page' : undefined}
          >
            Статистика
          </Link>
        )}
      </nav>
      <div className="app-header__auth">
        {token ? <UserMenu /> : <Link to="/login">Войти</Link>}
      </div>
    </header>
  );
}