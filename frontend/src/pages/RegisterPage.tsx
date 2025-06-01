import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Container,
  Paper,
  TextField,
  Typography,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import { api } from '../api/instance';
import type { GenderEnum } from '../api/api';
import { useAuthContext } from '../contexts/AuthContext';

export const RegisterPage = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const { login } = useAuthContext();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setLoading(true);

    const formData = new FormData(event.currentTarget);
    const data = {
      username: formData.get('username') as string,
      password: formData.get('password') as string,
      password2: formData.get('password2') as string,
      first_name: formData.get('firstName') as string,
      last_name: formData.get('lastName') as string,
      patronymic: formData.get('patronymic') as string || undefined,
      email: formData.get('email') as string || undefined,
      phone: formData.get('phone') as string || undefined,
      gender: formData.get('gender') as GenderEnum,
    };

    try {
      await api.api.v0RegistrationCreate(data);
      login(data.username);
      navigate('/equipment');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка при регистрации');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container component="main" maxWidth="sm">
      <Box
        sx={{
          marginTop: { xs: 2, sm: 8 },
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          px: isMobile ? 2 : 0,
          mb: 4,
        }}
      >
        <Paper 
          elevation={3} 
          sx={{ 
            p: { xs: 2, sm: 4 }, 
            width: '100%',
            maxWidth: '100%',
          }}
        >
          <Typography component="h1" variant="h5" align="center" gutterBottom>
            Регистрация
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} noValidate>
            <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' } }}>
              <Box sx={{ gridColumn: '1/-1' }}>
                <TextField
                  required
                  fullWidth
                  id="username"
                  label="Имя пользователя"
                  name="username"
                  autoComplete="username"
                  size={isMobile ? "small" : "medium"}
                />
              </Box>
              <TextField
                required
                fullWidth
                name="password"
                label="Пароль"
                type="password"
                id="password"
                size={isMobile ? "small" : "medium"}
              />
              <TextField
                required
                fullWidth
                name="password2"
                label="Подтверждение пароля"
                type="password"
                id="password2"
                size={isMobile ? "small" : "medium"}
              />
              <TextField
                required
                fullWidth
                name="firstName"
                label="Имя"
                id="firstName"
                size={isMobile ? "small" : "medium"}
              />
              <TextField
                required
                fullWidth
                name="lastName"
                label="Фамилия"
                id="lastName"
                size={isMobile ? "small" : "medium"}
              />
              <Box sx={{ gridColumn: '1/-1' }}>
                <TextField
                  fullWidth
                  name="patronymic"
                  label="Отчество"
                  id="patronymic"
                  size={isMobile ? "small" : "medium"}
                />
              </Box>
              <TextField
                fullWidth
                name="email"
                label="Email"
                type="email"
                id="email"
                size={isMobile ? "small" : "medium"}
              />
              <TextField
                fullWidth
                name="phone"
                label="Телефон"
                id="phone"
                size={isMobile ? "small" : "medium"}
              />
              <Box sx={{ gridColumn: '1/-1' }}>
                <FormControl fullWidth size={isMobile ? "small" : "medium"}>
                  <InputLabel id="gender-label">Пол</InputLabel>
                  <Select
                    labelId="gender-label"
                    id="gender"
                    name="gender"
                    label="Пол"
                    defaultValue="U"
                  >
                    <MenuItem value="M">Мужской</MenuItem>
                    <MenuItem value="F">Женский</MenuItem>
                    <MenuItem value="U">Не указан</MenuItem>
                  </Select>
                </FormControl>
              </Box>
            </Box>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
            >
              {loading ? 'Регистрация...' : 'Зарегистрироваться'}
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}; 