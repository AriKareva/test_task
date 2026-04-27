import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { lazy, Suspense } from 'react';
import Layout from './shared/components/Layout';
import ProtectedRoute from './shared/components/ProtectedRoute';

const AllTasksPage = lazy(() => import('./pages/AllTasksPage'));
const MyTasksPage = lazy(() => import('./pages/MyTasksPage'));
const AnalyticsPage = lazy(() => import('./pages/AnalyticsPage'));
const LoginPage = lazy(() => import('./pages/LoginPage'));
const RegisterPage = lazy(() => import('./pages/RegisterPage'));

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      refetchOnWindowFocus: false,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Suspense fallback={<div className="loading">Loading...</div>}>
          <Routes>
            <Route element={<Layout />}>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route element={<ProtectedRoute />}>
                <Route path="/tasks" element={<AllTasksPage />} />
                <Route path="/my-tasks" element={<MyTasksPage />} />
                {/* <Route path="/analytics" element={<AnalyticsPage />} /> */}
                <Route path="/" element={<Navigate to="/tasks" replace />} />
              </Route>
            </Route>
          </Routes>
        </Suspense>
      </BrowserRouter>
    </QueryClientProvider>
  );
}