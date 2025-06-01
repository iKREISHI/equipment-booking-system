import { Box, Container, Paper, Typography, useTheme, useMediaQuery } from '@mui/material';
import InventoryIcon from '@mui/icons-material/Inventory';

export const HomePage = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <Container maxWidth="lg" sx={{ mt: { xs: 2, sm: 4 }, px: { xs: 1, sm: 3 } }}>
      <Paper elevation={3} sx={{ p: { xs: 2, sm: 4 } }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: { xs: 2, sm: 4 }, flexDirection: isMobile ? 'column' : 'row' }}>
          <InventoryIcon sx={{ fontSize: { xs: 32, sm: 40 }, mr: isMobile ? 0 : 2, mb: isMobile ? 1 : 0 }} />
          <Typography variant="h4" component="h1" sx={{ 
            fontSize: { xs: '1.5rem', sm: '2.125rem' },
            textAlign: isMobile ? 'center' : 'left',
          }}>
            Система управления оборудованием
          </Typography>
        </Box>
        
        <Typography variant="h6" gutterBottom sx={{ fontSize: { xs: '1.1rem', sm: '1.25rem' } }}>
          Добро пожаловать в систему управления оборудованием!
        </Typography>
        
        <Typography paragraph sx={{ fontSize: { xs: '0.875rem', sm: '1rem' } }}>
          Наша система позволяет эффективно управлять оборудованием в организации:
        </Typography>
        
        <Box component="ul" sx={{ pl: { xs: 3, sm: 4 } }}>
          <Typography component="li" sx={{ fontSize: { xs: '0.875rem', sm: '1rem' }, mb: 1 }}>
            Учет и инвентаризация оборудования
          </Typography>
          <Typography component="li" sx={{ fontSize: { xs: '0.875rem', sm: '1rem' }, mb: 1 }}>
            Отслеживание местоположения
          </Typography>
          <Typography component="li" sx={{ fontSize: { xs: '0.875rem', sm: '1rem' }, mb: 1 }}>
            Управление статусами оборудования
          </Typography>
          <Typography component="li" sx={{ fontSize: { xs: '0.875rem', sm: '1rem' }, mb: 1 }}>
            Бронирование и планирование использования
          </Typography>
          <Typography component="li" sx={{ fontSize: { xs: '0.875rem', sm: '1rem' } }}>
            Контроль технического обслуживания
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
}; 