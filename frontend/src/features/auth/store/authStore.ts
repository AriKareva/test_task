import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  accessToken: string | null;
  userId: number | null;
  username: string | null;
  login: (token: string, userId: number, username: string) => void;  
  logout: () => void;                                     
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      userId: null,
      username: null,
      login: (token, userId, username) => set({ accessToken: token, userId, username }),
      logout: () => set({ accessToken: null, userId: null, username: null }),
    }),
    { name: 'auth-storage' }
  )
);