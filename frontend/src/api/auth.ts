import axios from './axios';

export const loginUser = (login: string, password: string) =>
  axios.post('/users/signin', { login, password }).then(res => res.data);

export const registerUser = (login: string, password: string, email: string) =>
  axios.post('/users/', { login, password, email }).then(res => res.data);