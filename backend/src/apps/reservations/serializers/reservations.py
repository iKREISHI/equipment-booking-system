from rest_framework import serializers
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.reservations.models import Reservation
from apps.equipments.models.inventory_equipment import InventoryEquipment
from apps.locations.models import Location
from apps.users.models import User


class ReservationSerializer(serializers.ModelSerializer):
    """
    Сериализатор аренды инвентарного оборудования.

    • На запись принимает `equipment`, `renter`, `assigned_by`, `location`
      как **ID** связанных объектов.
    • Отдаёт читаемые поля: имя оборудования, пользователи, локация.
    • Валидирует даты и проверяет перекрытия для одного и того же оборудования.
    """

    equipment = serializers.PrimaryKeyRelatedField(
        queryset=InventoryEquipment.objects.all(),
        help_text=_("ID оборудования"),
    )
    renter = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text=_("ID арендатора"),
    )
    assigned_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text=_("ID пользователя, оформившего аренду"),
    )
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        help_text=_("ID местоположения оборудования"),
    )

    equipment_name = serializers.CharField(source="equipment.name", read_only=True)
    renter_username = serializers.CharField(source="renter.username", read_only=True)
    assigned_by_username = serializers.CharField(
        source="assigned_by.username", read_only=True
    )
    location_name = serializers.CharField(source="location.name", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "equipment", "renter", "assigned_by", "location",
            "equipment_name", "renter_username", "assigned_by_username", "location_name",
            "start_time", "end_time", "actual_return_time",
            "description",
        ]
        read_only_fields = [
            "id", "start_time",
            "equipment_name", "renter_username", "assigned_by_username", "location_name",
        ]

    def validate_end_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                _("Время окончания должно быть в будущем.")
            )
        return value

    def validate_actual_return_time(self, value):
        if value and value <= timezone.now():
            # Возврат в прошлом разрешаем — главное, чтобы он был после старта
            return value
        return value

    def validate(self, attrs):
        start_time = (
            self.instance.start_time
            if self.instance
            else timezone.now()
        )
        end_time = attrs.get("end_time") or getattr(self.instance, "end_time", None)
        if end_time and end_time <= start_time:
            raise serializers.ValidationError({
                "end_time": _("Время окончания должно быть позже времени начала.")
            })

        actual_return = attrs.get("actual_return_time")
        if actual_return and actual_return < start_time:
            raise serializers.ValidationError({
                "actual_return_time": _("Фактический возврат не может быть раньше начала аренды.")
            })

        # Проверка перекрытий
        equipment = attrs.get("equipment") or self.instance.equipment
        qs = Reservation.objects.filter(equipment=equipment)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        overlap = qs.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            actual_return_time__isnull=True,
        ).exists()
        if overlap:
            raise serializers.ValidationError(
                _("Указанный интервал перекрывается с существующей арендой этого оборудования.")
            )

        return attrs
