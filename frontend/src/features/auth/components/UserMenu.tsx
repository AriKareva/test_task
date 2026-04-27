import { useState, useRef, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';

export default function UserMenu() {
  const { username, logout } = useAuthStore();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  return (
    <div className="user-menu" ref={ref}>
      <button className="user-menu__toggle" onClick={() => setOpen(!open)}>
        {username}
      </button>
      {open && (
        <div className="user-menu__dropdown">
          <button onClick={logout}>Выйти</button>
        </div>
      )}
    </div>
  );
}