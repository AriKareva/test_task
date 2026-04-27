// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw';
import { users, tasks } from './data';

// Простейшая генерация фейкового токена
let nextTaskId = tasks.length + 1;

export const handlers = [
  // ----------------- Аутентификация -----------------
  http.post('*/auth/login', async ({ request }) => {
    const body: any = await request.json();
    const user = users.find(u => u.login === body.login && u.password === body.password);
    if (!user) {
      return HttpResponse.json({ detail: 'Invalid credentials' }, { status: 401 });
    }
    const token = `fake-jwt-${user.user_id}-${Date.now()}`;
    return HttpResponse.json({
      access_token: token,
      user_id: user.user_id,
      login: user.login,
    });
  }),

  http.post('*/auth/signup', async ({ request }) => {
    const body: any = await request.json();
    const newUser = {
      user_id: users.length + 1,
      login: body.login,
      password: body.password,
      email: body.email,
    };
    users.push(newUser);
    const token = `fake-jwt-${newUser.user_id}-${Date.now()}`;
    return HttpResponse.json({
      access_token: token,
      user_id: newUser.user_id,
      login: newUser.login,
    }, { status: 201 });
  }),

  // ----------------- Задачи -----------------
  http.get('*/tasks', () => {
    // Все задачи
    return HttpResponse.json(tasks);
  }),

  http.get('*/tasks/user/:userId', ({ params }) => {
    const userId = Number(params.userId);
    const userTasks = tasks.filter(t => t.assignee_id === userId);
    return HttpResponse.json(userTasks);
  }),

  http.post('*/tasks', async ({ request }) => {
    const body: any = await request.json();
    const newTask = {
      task_id: nextTaskId++,
      task_title: body.task_title,
      description: body.description || null,
      author_id: 1, // предположим, что автор – текущий пользователь (можно достать из токена позже)
      current_status: 'Создана',
      assignee_id: null,
    };
    tasks.push(newTask);
    return HttpResponse.json(newTask, { status: 201 });
  }),

  http.patch('*/tasks/:taskId/status', async ({ params, request }) => {
    const taskId = Number(params.taskId);
    const body: any = await request.json();
    const task = tasks.find(t => t.task_id === taskId);
    if (!task) return HttpResponse.json({ detail: 'Not found' }, { status: 404 });
    const statusMap: Record<number, string> = {
      1: 'Создана',
      2: 'В работе',
      3: 'Выполнена',
    };
    task.current_status = statusMap[body.status_id] || task.current_status;
    return HttpResponse.json(task);
  }),

  // ----------------- Статистика -----------------
  http.get('*/statistics/status-avg-time', () => {
    return HttpResponse.json([
      { status_title: 'Создана', avg_minutes: 120.5 },
      { status_title: 'В работе', avg_minutes: 340.2 },
      { status_title: 'Выполнена', avg_minutes: 0 },
    ]);
  }),

  http.get('*/statistics/top-productive-users', ({ request }) => {
    const url = new URL(request.url);
    const limit = Number(url.searchParams.get('limit')) || 3;
    const result = [
      { user_id: 1, login: 'alice', avg_minutes: 45.3 },
      { user_id: 3, login: 'charlie', avg_minutes: 67.8 },
      { user_id: 2, login: 'bob', avg_minutes: 112.4 },
    ].slice(0, limit);
    return HttpResponse.json(result);
  }),
];