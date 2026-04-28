import axios from './axios';

interface Task {
    description?: string | null;
    priority?: number | null;
    assignee_id?: number | null;
    author_id?: number | null;
    task_id?: number | null;
    task_title?: string | null;
    current_status?: string | null;
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
    // data: { task_title: string; description?: string }
) =>
    console.log('работает');
//   axios.post<Task>('/tasks/', data).then(res => res.data);

// Универсальное обновление (можно передать любые поля, в том числе status_id)
export const updateTask = (
// taskId: number, data: Record<string, any>

) =>
    console.log('работает');
//   axios.patch<Task>(`/tasks/${taskId}`, data).then(res => res.data);

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
    // taskId: number
) =>
    console.log('работает');
//   axios.delete(`/tasks/${taskId}`).then(res => res.data);