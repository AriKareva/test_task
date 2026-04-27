import axios from './axios';

export const loginUser = (login: string, password: string) =>
  axios.post('/auth/login', { login, password }).then(res => res.data);

export const registerUser = (login: string, password: string, email: string) =>
  axios.post('/auth/signup', { login, password, email }).then(res => res.data);