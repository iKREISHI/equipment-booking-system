import { useState, useEffect } from 'react';
import { api } from '../api/instance';
import type { InventoryEquipment, PaginatedInventoryEquipmentList } from '../api/api';

export const EquipmentList = () => {
  const [equipment, setEquipment] = useState<InventoryEquipment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEquipment = async () => {
      try {
        const response = await api.api.v0InventoryEquipmentList();
        const data = response.data as PaginatedInventoryEquipmentList;
        setEquipment(data.results);
      } catch (err) {
        setError('Ошибка при загрузке оборудования');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchEquipment();
  }, []);

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>Список оборудования</h1>
      <div className="equipment-grid">
        {equipment.map((item) => (
          <div key={item.id} className="equipment-card">
            <h3>{item.name}</h3>
            {item.photo && <img src={item.photo} alt={item.name} />}
            <p>Инвентарный номер: {item.inventory_number}</p>
            <p>Статус: {item.status_name}</p>
            <p>Местоположение: {item.location_name}</p>
            {item.description && <p>Описание: {item.description}</p>}
          </div>
        ))}
      </div>
    </div>
  );
}; 