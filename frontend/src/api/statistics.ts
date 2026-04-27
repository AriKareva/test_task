import axios from './axios';

export const fetchStatusAvgTime = () =>
  axios.get('/statistics/status-avg-time').then(res => res.data);

export const fetchTopProductiveUsers = (limit = 3) =>
  axios.get('/statistics/top-productive-users', { params: { limit } }).then(res => res.data);