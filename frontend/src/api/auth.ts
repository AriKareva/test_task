import axios from './axios';

export const loginUser = (login: string, password: string) =>
  axios.post('/user/signin', { login, password }).then(res => res.data);

export const registerUser = (login: string, password: string, email: string) =>
  axios.post('/user/', { login, password, email }).then(res => res.data);