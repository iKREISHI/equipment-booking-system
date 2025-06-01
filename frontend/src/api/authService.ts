import api from './axiosConfig';

interface LoginPayload {
  username: string;
  password: string;
}

interface LoginResponse {
  // Здесь поля, которые может вернуть ваш DRF-view.
  // Если вы возвращаете в JSON дополнительные данных о пользователе — пропишите их:
  // например, { user_id: number, email: string, ... }
  detail?: string; // если DRF отдаёт сообщение об успешном входе
}

/**
 * Отправляет данные на /auth/login/ для создания сессии. 
 * DRF будет устанавливать куку 'sessionid' и 'csrftoken'.
 */
export const login = async (payload: LoginPayload): Promise<LoginResponse> => {
  const response = await api.post<LoginResponse>('/auth/login/', payload);
  return response.data;
};

/**
 * Отправляет запрос logout: DRF уничтожает сессию, куки инвалидируются.
 */
export const logout = async (): Promise<void> => {
  await api.post('/auth/logout/');
};
