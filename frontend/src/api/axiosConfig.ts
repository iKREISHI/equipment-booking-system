import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse, AxiosError } from 'axios';

/**
 * Функция для чтения CSRF-токена из document.cookie.
 * Django выдаёт куку 'csrftoken' после первой загрузки страницы.
 */
function getCsrfToken(): string | null {
  const csrfCookieName = 'csrftoken';
  if (typeof document === 'undefined' || !document.cookie) {
    return null;
  }
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(`${csrfCookieName}=`)) {
      return decodeURIComponent(cookie.substring(csrfCookieName.length + 1));
    }
  }
  return null;
}

// Интерфейс расширения AxiosRequestConfig, если нужно добавлять поля
interface CustomAxiosConfig extends AxiosRequestConfig {}

// Создаём инстанс Axios
const api: AxiosInstance = axios.create({
  // Задаём базовый URL вашего бэкенда (DRF). 
  // Можно переопределить через .env: REACT_APP_API_URL
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v0/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  // Важно: сессионная аутентификация DRF опирается на куки, поэтому нужно withCredentials.
  withCredentials: true,
});

// --- Request Interceptor: автоматически добавляем X-CSRFToken ---
api.interceptors.request.use(
  (config: CustomAxiosConfig) => {
    // Берём CSRF-токен из куки (cookie name = 'csrftoken')
    const csrfToken = getCsrfToken();
    if (csrfToken) {
      config.headers = {
        ...config.headers,
        'X-CSRFToken': csrfToken,
      };
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// --- Response Interceptor: обрабатываем 401/403 и т.д. ---
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    if (error.response) {
      const status = error.response.status;
      if (status === 401) {
        // Пользователь не аутентифицирован, можно редиректить на /login
        // Или сохранять state ошибки
        console.warn('401 Unauthorized: пользователь не аутентифицирован.');
        // Например, можно window.location.href = '/login';
      } else if (status === 403) {
        // Запрос запрещён — может не хватать прав
        console.warn('403 Forbidden: недостаточно прав.');
      }
    }
    return Promise.reject(error);
  }
);

export default api;
