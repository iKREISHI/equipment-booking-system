import React from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Avatar,
  Divider
} from '@mui/material';
import { useAuth } from '../hooks/useAuth';
import AccountCircle from '@mui/icons-material/AccountCircle';

export const ProfilePage = () => {
  const { user } = useAuth();

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <Avatar sx={{ width: 100, height: 100, mr: 3 }}>
            <AccountCircle sx={{ width: 80, height: 80 }} />
          </Avatar>
          <Box>
            <Typography variant="h4" gutterBottom>
              {user?.username}
            </Typography>
            <Typography variant="body1" color="textSecondary">
              ID: {user?.user_id}
            </Typography>
          </Box>
        </Box>

        <Divider sx={{ my: 3 }} />

        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
          <Box sx={{ flexBasis: { xs: '100%', sm: '45%' } }}>
            <Typography variant="subtitle2" color="textSecondary">
              Имя пользователя
            </Typography>
            <Typography variant="body1">{user?.username}</Typography>
          </Box>
          
          <Box sx={{ flexBasis: { xs: '100%', sm: '45%' } }}>
            <Typography variant="subtitle2" color="textSecondary">
              Статус
            </Typography>
            <Typography variant="body1">Активный</Typography>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
}; 