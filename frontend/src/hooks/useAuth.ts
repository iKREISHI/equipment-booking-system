import { useState, useEffect } from 'react';

interface AuthUser {
  username: string;
  isAuthenticated: boolean;
}

export const useAuth = () => {
  const [user, setUser] = useState<AuthUser | null>(() => {
    const savedUser = localStorage.getItem('auth_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem('auth_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('auth_user');
    }
  }, [user]);

  const login = (username: string) => {
    setUser({ username, isAuthenticated: true });
  };

  const logout = () => {
    localStorage.clear();
    setUser(null);
  };

  return { user, login, logout };
}; 