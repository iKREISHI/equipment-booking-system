import axiosInstance from '../utils/axios';

interface LoginResponse {
  detail: string;
  user_id: number;
  username: string;
}

interface LoginData {
  username: string;
  password: string;
}

interface RegistrationData {
  username: string;
  password: string;
  password2: string;
  last_name: string;
  first_name: string;
  patronymic?: string;
  gender: 'M' | 'F' | 'U';
  email?: string;
  phone?: string;
  avatar?: string;
}

// Функция для очистки куки
const deleteCookie = (name: string) => {
  document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
};

class AuthService {
  async login(data: LoginData): Promise<LoginResponse> {
    try {
      const response = await axiosInstance.post<LoginResponse>('/login/', data);
      
      if (response.data.username) {
        const userData = {
          username: response.data.username,
          user_id: response.data.user_id
        };
        localStorage.setItem('user', JSON.stringify(userData));
      }
      
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async logout(): Promise<void> {
    try {
      await axiosInstance.post('/logout/');
      // Очищаем localStorage
      localStorage.removeItem('user');
      
      // Очищаем куки сессии и CSRF
      deleteCookie('sessionid');
      deleteCookie('csrftoken');
      
      // Для надежности очищаем все куки, связанные с доменом
      document.cookie.split(';').forEach(cookie => {
        const [name] = cookie.split('=');
        deleteCookie(name.trim());
      });

    } catch (error) {
      // Даже если запрос не удался, очищаем все данные
      localStorage.removeItem('user');
      deleteCookie('sessionid');
      deleteCookie('csrftoken');
      throw error;
    }
  }

  async register(data: RegistrationData): Promise<any> {
    try {
      const response = await axiosInstance.post('/registration/', data);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  getCurrentUser(): Partial<LoginResponse> | null {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      return JSON.parse(userStr);
    }
    return null;
  }

  isAuthenticated(): boolean {
    return !!this.getCurrentUser();
  }
}

export const authService = new AuthService(); 