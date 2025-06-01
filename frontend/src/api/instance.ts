import { Api } from './api';

export const api = new Api({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true, // Важно для работы с куками
  headers: {
    'Content-Type': 'application/json',
  },
}); 