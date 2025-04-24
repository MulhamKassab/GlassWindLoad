import axios from 'axios';

const instance = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  headers: { 'Content-Type': 'application/json' }
});

export const calculate = async (payload) => {
  const { data } = await instance.post('/calculate', payload);
  return data;
};

export default instance;
