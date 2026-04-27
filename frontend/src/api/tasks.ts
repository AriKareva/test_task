import axios from './axios';
import { Task } from '../features/tasks/types';

export const fetchAllTasks = () =>
  axios.get<Task[]>('/tasks').then(res => res.data);

export const fetchMyTasks = (userId: number) =>
  axios.get<Task[]>(`/tasks/user/${userId}`).then(res => res.data);

export const createTask = (data: { task_title: string; description?: string }) =>
  axios.post<Task>('/tasks', data).then(res => res.data);

export const updateTaskStatus = (taskId: number, statusId: number) =>
  axios.patch<Task>(`/tasks/${taskId}/status`, { status_id: statusId }).then(res => res.data);