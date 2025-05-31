from rest_framework import serializers
from apps.maintenance.models.maintenance import Maintenance
from apps.equipments.models import InventoryEquipment
from apps.maintenance.models.maintenance_status import MaintenanceStatus
from apps.users.models import User


class MaintenanceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Maintenance — обслуживания/проверки оборудования.
    Поля:
      - equipment: ссылка на InventoryEquipment (PrimaryKey)
      - reporter_by: ссылка на User, кто сообщил о проверке
      - assigned_by: ссылка на User, кто выполнял проверку
      - description: описание самой проверки (может быть пустым)
      - status: ссылка на MaintenanceStatus
      - created_at: автоматически ставится при создании (только для чтения)
      - updated_at: автоматически обновляется при изменении (только для чтения)
      - description_updated: описание изменений (может быть пустым)
      - start_time: дата и время начала обслуживания
      - end_time: дата и время конца обслуживания
    """

    # При необходимости можно вывести связанные модели через их __str__:
    equipment_display = serializers.CharField(
        source='equipment.__str__',
        read_only=True,
        label='Оборудование (строка)'
    )
    reporter_display = serializers.CharField(
        source='reporter_by.__str__',
        read_only=True,
        label='Reporter (строка)'
    )
    assigned_display = serializers.CharField(
        source='assigned_by.__str__',
        read_only=True,
        label='Assigned (строка)'
    )
    status_display = serializers.CharField(
        source='status.__str__',
        read_only=True,
        label='Статус (строка)'
    )

    class Meta:
        model = Maintenance
        # Поля, которые попадут в API-запрос и в ответ
        fields = (
            'id',
            'equipment',
            'equipment_display',
            'reporter_by',
            'reporter_display',
            'assigned_by',
            'assigned_display',
            'description',
            'status',
            'status_display',
            'created_at',
            'updated_at',
            'description_updated',
            'start_time',
            'end_time',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
            # Поля _display в любом случае только для чтения
            'equipment_display',
            'reporter_display',
            'assigned_display',
            'status_display',
        )
        extra_kwargs = {
            # Оборудование, репортер, ассигнер и статус — обязательные поля
            'equipment': {'required': True},
            'reporter_by': {'required': True},
            'assigned_by': {'required': True},
            'status': {'required': True},
            # Описание проверки может быть пустым
            'description': {'required': False, 'allow_blank': True},
            # Описание обновления может быть пустым
            'description_updated': {'required': False, 'allow_blank': True},
            # Даты начала/конца обязательны, проверку на порядок (start_time < end_time)
            # можно добавить в методе validate()
            'start_time': {'required': True},
            'end_time': {'required': True},
        }

    def validate(self, attrs):
        """
        Дополнительная валидация: проверяем, что start_time < end_time.
        """
        start = attrs.get('start_time') or getattr(self.instance, 'start_time', None)
        end = attrs.get('end_time') or getattr(self.instance, 'end_time', None)

        if start and end and start > end:
            raise serializers.ValidationError({
                'end_time': 'Время окончания обслуживания должно быть позже времени начала.'
            })
        return attrs
