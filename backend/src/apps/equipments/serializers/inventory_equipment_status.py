from rest_framework import serializers
from apps.equipments.models import InventoryEquipmentStatus


class InventoryEquipmentStatusSerializer(serializers.ModelSerializer):
    """
    Сериализатор статуса инвентарного оборудования.
    Передаёт / принимает только поле ``name`` (и ``id`` как read-only).
    """

    class Meta:
        model = InventoryEquipmentStatus
        fields = ["id", "name"]
        read_only_fields = ["id"]

    def validate_name(self, value: str) -> str:
        normalized = value.casefold().strip()

        qs = InventoryEquipmentStatus.objects.all()
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        # сравниваем через Python (в БД-агностичной манере)
        duplicates = [
            obj for obj in qs.only("name")
            if obj.name.casefold().strip() == normalized
        ]
        if duplicates:
            raise serializers.ValidationError("Такой статус уже существует.")

        return value
