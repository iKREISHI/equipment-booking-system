import { useState } from 'react';
import { AppBar, Box, Button, Container, IconButton, Menu, MenuItem, Toolbar, Typography, useTheme, useMediaQuery } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import MenuIcon from '@mui/icons-material/Menu';
import { api } from '../../api/instance';
import { useAuthContext } from '../../contexts/AuthContext';

export const Navbar = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const { user, logout: authLogout } = useAuthContext();
  
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = async () => {
    try {
      await api.api.v0LogoutCreate();
      authLogout();
      navigate('/login');
    } catch (error) {
      console.error('Ошибка при выходе:', error);
    }
    handleClose();
  };

  const menuItems = user ? (
    <>
      <Button
        component={Link}
        to="/equipment"
        sx={{ color: 'white' }}
        onClick={handleClose}
      >
        Оборудование
      </Button>
      <Button
        onClick={handleLogout}
        sx={{ color: 'white' }}
      >
        Выход ({user.username})
      </Button>
    </>
  ) : (
    <>
      <Button
        component={Link}
        to="/login"
        sx={{ color: 'white' }}
        onClick={handleClose}
      >
        Вход
      </Button>
      <Button
        component={Link}
        to="/register"
        sx={{ color: 'white' }}
        onClick={handleClose}
      >
        Регистрация
      </Button>
    </>
  );

  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            noWrap
            component={Link}
            to="/"
            sx={{
              mr: 2,
              display: 'flex',
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
              flexGrow: isMobile ? 1 : 0,
            }}
          >
            EQUIPMENT
          </Typography>

          {isMobile ? (
            <>
              <IconButton
                size="large"
                edge="end"
                color="inherit"
                aria-label="menu"
                onClick={handleMenu}
              >
                <MenuIcon />
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                anchorOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                keepMounted
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                {user && (
                  <MenuItem component={Link} to="/equipment" onClick={handleClose}>
                    Оборудование
                  </MenuItem>
                )}
                {!user && (
                  <>
                    <MenuItem component={Link} to="/login" onClick={handleClose}>
                      Вход
                    </MenuItem>
                    <MenuItem component={Link} to="/register" onClick={handleClose}>
                      Регистрация
                    </MenuItem>
                  </>
                )}
                {user && (
                  <MenuItem onClick={handleLogout}>
                    Выход ({user.username})
                  </MenuItem>
                )}
              </Menu>
            </>
          ) : (
            <Box sx={{ display: 'flex', gap: 2, ml: 'auto' }}>
              {menuItems}
            </Box>
          )}
        </Toolbar>
      </Container>
    </AppBar>
  );
}; 