import { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Container,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Fab,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TextField,
  Typography,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { api } from '../api/instance';
import type {
  InventoryEquipment,
  PaginatedInventoryEquipmentList,
  PatchedInventoryEquipment,
} from '../api/api';

interface EquipmentFormData {
  name: string;
  inventory_number: string;
  description?: string;
  location: number;
  status?: number;
  owner: number;
}

export const EquipmentPage = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [equipment, setEquipment] = useState<InventoryEquipment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [totalCount, setTotalCount] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  // Модальные окна
  const [openAdd, setOpenAdd] = useState(false);
  const [openEdit, setOpenEdit] = useState(false);
  const [openDelete, setOpenDelete] = useState(false);
  const [selectedEquipment, setSelectedEquipment] = useState<InventoryEquipment | null>(null);

  const fetchEquipment = async () => {
    try {
      setLoading(true);
      const response = await api.api.v0InventoryEquipmentList({
        page: page + 1,
        page_size: rowsPerPage,
      });
      const data = response.data as PaginatedInventoryEquipmentList;
      setEquipment(data.results);
      setTotalCount(data.count);
    } catch (err) {
      setError('Ошибка при загрузке оборудования');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEquipment();
  }, [page, rowsPerPage]);

  const handleChangePage = (_: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleAdd = async (formData: EquipmentFormData) => {
    try {
      const newEquipment: InventoryEquipment = {
        ...formData,
        id: 0, // Будет присвоен сервером
        owner_username: '', // Будет заполнено сервером
        status_name: '', // Будет заполнено сервером
        location_name: '', // Будет заполнено сервером
        registration_date: new Date().toISOString().split('T')[0], // Текущая дата
        created_at: null,
        updated_at: null,
        photo: null,
      };
      await api.api.v0InventoryEquipmentCreate(newEquipment);
      fetchEquipment();
      setOpenAdd(false);
    } catch (err) {
      console.error('Ошибка при добавлении:', err);
    }
  };

  const handleEdit = async (id: number, formData: PatchedInventoryEquipment) => {
    try {
      await api.api.v0InventoryEquipmentPartialUpdate(id, formData);
      fetchEquipment();
      setOpenEdit(false);
    } catch (err) {
      console.error('Ошибка при редактировании:', err);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.api.v0InventoryEquipmentDestroy(id);
      fetchEquipment();
      setOpenDelete(false);
    } catch (err) {
      console.error('Ошибка при удалении:', err);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, px: { xs: 1, sm: 3 } }}>
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1" sx={{ fontSize: { xs: '1.5rem', sm: '2.125rem' } }}>
          Оборудование
        </Typography>
        <Fab
          color="primary"
          aria-label="add"
          onClick={() => setOpenAdd(true)}
          size={isMobile ? "small" : "medium"}
        >
          <AddIcon />
        </Fab>
      </Box>

      <TableContainer component={Paper}>
        <Table size={isMobile ? "small" : "medium"}>
          <TableHead>
            <TableRow>
              <TableCell>Название</TableCell>
              {!isMobile && <TableCell>Инв. номер</TableCell>}
              <TableCell>Статус</TableCell>
              {!isMobile && <TableCell>Местоположение</TableCell>}
              <TableCell align="right">Действия</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {equipment.map((item) => (
              <TableRow key={item.id}>
                <TableCell>{item.name}</TableCell>
                {!isMobile && <TableCell>{item.inventory_number}</TableCell>}
                <TableCell>{item.status_name}</TableCell>
                {!isMobile && <TableCell>{item.location_name}</TableCell>}
                <TableCell align="right">
                  <IconButton
                    onClick={() => {
                      setSelectedEquipment(item);
                      setOpenEdit(true);
                    }}
                    size={isMobile ? "small" : "medium"}
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    onClick={() => {
                      setSelectedEquipment(item);
                      setOpenDelete(true);
                    }}
                    size={isMobile ? "small" : "medium"}
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={totalCount}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          labelRowsPerPage={isMobile ? "Строк:" : "Строк на странице:"}
        />
      </TableContainer>

      {/* Модальное окно добавления */}
      <Dialog 
        open={openAdd} 
        onClose={() => setOpenAdd(false)}
        fullScreen={isMobile}
      >
        <DialogTitle>Добавить оборудование</DialogTitle>
        <DialogContent>
          <Box component="form" id="add-equipment-form" onSubmit={(e) => {
            e.preventDefault();
            const formData = new FormData(e.currentTarget);
            handleAdd({
              name: formData.get('name') as string,
              inventory_number: formData.get('inventory_number') as string,
              description: formData.get('description') as string || undefined,
              location: Number(formData.get('location')),
              status: formData.get('status') ? Number(formData.get('status')) : undefined,
              owner: Number(formData.get('owner')),
            });
          }} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="name"
              label="Название"
              name="name"
              autoFocus
              size={isMobile ? "small" : "medium"}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="inventory_number"
              label="Инвентарный номер"
              name="inventory_number"
              size={isMobile ? "small" : "medium"}
            />
            <TextField
              margin="normal"
              fullWidth
              id="description"
              label="Описание"
              name="description"
              multiline
              rows={4}
              size={isMobile ? "small" : "medium"}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="location"
              label="ID местоположения"
              name="location"
              type="number"
              size={isMobile ? "small" : "medium"}
            />
            <TextField
              margin="normal"
              fullWidth
              id="status"
              label="ID статуса"
              name="status"
              type="number"
              size={isMobile ? "small" : "medium"}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="owner"
              label="ID владельца"
              name="owner"
              type="number"
              size={isMobile ? "small" : "medium"}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAdd(false)}>Отмена</Button>
          <Button type="submit" form="add-equipment-form">
            Добавить
          </Button>
        </DialogActions>
      </Dialog>

      {/* Модальное окно редактирования */}
      <Dialog 
        open={openEdit} 
        onClose={() => setOpenEdit(false)}
        fullScreen={isMobile}
      >
        <DialogTitle>Редактировать оборудование</DialogTitle>
        <DialogContent>
          <Box component="form" id="edit-equipment-form" onSubmit={(e) => {
            e.preventDefault();
            if (!selectedEquipment) return;
            
            const formData = new FormData(e.currentTarget);
            const updatedData: PatchedInventoryEquipment = {
              name: formData.get('name') as string,
              inventory_number: formData.get('inventory_number') as string,
              description: formData.get('description') as string || undefined,
              location: Number(formData.get('location')),
              status: formData.get('status') ? Number(formData.get('status')) : undefined,
              owner: Number(formData.get('owner')),
            };
            handleEdit(selectedEquipment.id, updatedData);
          }} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="name"
              label="Название"
              name="name"
              defaultValue={selectedEquipment?.name}
              size={isMobile ? "small" : "medium"}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="inventory_number"
              label="Инвентарный номер"
              name="inventory_number"
              defaultValue={selectedEquipment?.inventory_number}
              size={isMobile ? "small" : "medium"}
            />
            <TextField
              margin="normal"
              fullWidth
              id="description"
              label="Описание"
              name="description"
              multiline
              rows={4}
              defaultValue={selectedEquipment?.description}
              size={isMobile ? "small" : "medium"}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="location"
              label="ID местоположения"
              name="location"
              type="number"
              defaultValue={selectedEquipment?.location}
              size={isMobile ? "small" : "medium"}
            />
            <TextField
              margin="normal"
              fullWidth
              id="status"
              label="ID статуса"
              name="status"
              type="number"
              defaultValue={selectedEquipment?.status}
              size={isMobile ? "small" : "medium"}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="owner"
              label="ID владельца"
              name="owner"
              type="number"
              defaultValue={selectedEquipment?.owner}
              size={isMobile ? "small" : "medium"}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEdit(false)}>Отмена</Button>
          <Button type="submit" form="edit-equipment-form">
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>

      {/* Модальное окно удаления */}
      <Dialog 
        open={openDelete} 
        onClose={() => setOpenDelete(false)}
        fullScreen={isMobile}
      >
        <DialogTitle>Удалить оборудование</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Вы действительно хотите удалить оборудование "{selectedEquipment?.name}"?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDelete(false)}>Отмена</Button>
          <Button
            onClick={() => selectedEquipment && handleDelete(selectedEquipment.id)}
            color="error"
          >
            Удалить
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}; 