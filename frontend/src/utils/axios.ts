import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/v0',
  withCredentials: true, // Важно для работы с сессионными куками
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest' // Добавляем заголовок для Django
  }
});

// Функция для проверки наличия куки
const getCookie = (name: string): string | null => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop()?.split(';').shift() || null;
  }
  return null;
};

// Добавляем перехватчик запросов для обработки CSRF токена
axiosInstance.interceptors.request.use(
  (config) => {
    // Получаем CSRF токен из куки
    const csrfToken = getCookie('csrftoken');

    // Добавляем CSRF токен только для небезопасных методов
    if (csrfToken && ['post', 'put', 'patch', 'delete'].includes(config.method?.toLowerCase() || '')) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Добавляем перехватчик ответов
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Проверяем статус ответа и наличие куки сессии
    if (
      error.response?.status === 401 || 
      error.response?.status === 403 || 
      !getCookie('sessionid')
    ) {
      // Очищаем localStorage
      localStorage.removeItem('user');
      
      // Если мы не на странице входа, перенаправляем
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance; 