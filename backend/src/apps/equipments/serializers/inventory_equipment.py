from rest_framework import serializers
from apps.equipments.models.inventory_equipment import InventoryEquipment
from apps.equipments.models.inventory_equipment_status import InventoryEquipmentStatus
from apps.locations.models import Location
from apps.users.models import User


class InventoryEquipmentSerializer(serializers.ModelSerializer):
    """
    Сериализатор инвентарного оборудования.

    * На запись принимает **id** связанных объектов (`owner`, `status`, `location`).
    * На чтение дополнительно отдаёт их «читаемые» имена.
    """

    # ──────────────── writeable FK поля ────────────────
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text="ID пользователя-владельца"
    )
    status = serializers.PrimaryKeyRelatedField(
        queryset=InventoryEquipmentStatus.objects.all(),
        allow_null=True, required=False,
        help_text="ID статуса оборудования"
    )
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        help_text="ID местоположения оборудования"
    )

    # ──────────────── read-only «читаемые» поля ────────────────
    owner_username = serializers.CharField(
        source="owner.username", read_only=True
    )
    status_name = serializers.CharField(
        source="status.name", read_only=True
    )
    location_name = serializers.CharField(
        source="location.name", read_only=True
    )

    class Meta:
        model = InventoryEquipment
        fields = [
            "id",
            # FK ids (write)
            "owner", "status", "location",
            # human-readables (read)
            "owner_username", "status_name", "location_name",
            # основные данные
            "name", "inventory_number", "photo", "description",
            # даты
            "registration_date", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "registration_date", "created_at", "updated_at",
            "owner_username", "status_name", "location_name",
        ]

    # ------------------------------------------------------------------
    # Валидации
    # ------------------------------------------------------------------
    def validate_inventory_number(self, value: str) -> str:
        """
        Штрих-код должен быть уникальным (без учёта регистра).
        """
        qs = InventoryEquipment.objects.filter(inventory_number__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "Оборудование с таким штрих-кодом уже существует."
            )
        return value

    def validate_photo(self, value):
        """
        Ограничиваем размер загружаемой фотографии 2 МБ.
        """
        if value and value.size > 2 * 1024 * 1024:  # 2 МБ
            raise serializers.ValidationError(
                "Размер фото не должен превышать 2 МБ."
            )
        return value
