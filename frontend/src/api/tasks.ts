import axios from './axios';

export interface TaskAssignee {
  assignee_id: number;
  assignee_login: string;
  assignee_dt: string;
}

export interface TaskStatus {
  status_id: number;
  status_title: string;
  status_dt: string;
}

export interface Task {
  task_id: number;
  task_title: string;
  description: string | null;
  author_id: number;
  author_login?: string | null;
  cur_assignee: TaskAssignee | null;
  current_status: TaskStatus | null;
  priority?: string | null;
  deadline?: string | null;
}

export interface StatusHistoryEntry {
  status_id: number;
  status_title: string;
  status_dt: string;
}

export interface PriorityHistoryEntry {
  priority_id: number;
  priority_title: string;
  priority_dt: string;
}


// Все задачи
export const fetchAllTasks = async () => {
    const res = await axios.get<Task[]>('/tasks/');
    return res.data;
  };


// Одна задача
export const fetchTaskById = async (
    taskId: number
) => {
  const res = await axios.get<Task>(`/tasks/${taskId}`).then(res => res.data)
  return res
};


// Создание задачи (author_id подставит бэкенд)
export const createTask = (
    data: { task_title: string; description?: string }
) =>
  axios.post<Task>('/tasks/', data).then(res => res.data);


// Универсальное обновление (можно передать любые поля, в том числе status_id)
export const updateTask = (
taskId: number, data: Record<string, any>
) =>
  axios.patch<Task>(`/tasks/${taskId}`, data).then(res => res.data);


// Задачи, где пользователь – автор
export const fetchUserCreatedTasks = async (
    userId: number

) => {
  const res = await axios.get<Task[]>(`/tasks/${userId}/created`).then(res => res.data)
  return res
};


// Задачи, где пользователь – исполнитель
export const fetchUserAssignedTasks = (userId: number) =>
    axios.get<Task[]>(`/tasks/${userId}/assigned`).then(res => res.data);


// Удаление
export const deleteTask = (
    taskId: number
) =>
  axios.delete(`/tasks/${taskId}`).then(res => res.data);

export const fetchStatuses = () =>
    axios.get<StatusItem[]>('/tasks/statuses').then(res => res.data);


export interface PriorityItem {
  priority_id: number;
  priority_title: string;
}

export const fetchPriorities = () =>
  axios.get<PriorityItem[]>('/tasks/priorities').then(res => res.data);


export const fetchTaskStatusHistory = (taskId: number) =>
  axios.get<StatusHistoryEntry[]>(`/tasks/${taskId}/status-history`).then(res => res.data);

export const fetchTaskPriorityHistory = (taskId: number) =>
  axios.get<PriorityHistoryEntry[]>(`/tasks/${taskId}/priority-history`).then(res => res.data);

export const updateTaskPriority = (taskId: number, priorityId: number) =>
  axios.patch<Task>(`/tasks/${taskId}/priority`, { priority_id: priorityId }).then(res => res.data);

export const updateTaskAssignee = (taskId: number, assigneeId: number) =>
  axios.patch(`/tasks/${taskId}/assignee`, { assignee_id: assigneeId }).then(res => res.data);

export interface User {
  user_id: number;
  user_login: string;
  user_email: string;
}

export const fetchUsers = () =>
  axios.get<User[]>('/users/').then(res => res.data);