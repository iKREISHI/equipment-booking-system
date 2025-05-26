from rest_framework import serializers
from apps.locations.models import Location        # поправьте путь к модели

class LocationSerializer(serializers.ModelSerializer):
    """
    Сериализатор местоположения инвентарного оборудования.
    Отдаёт / принимает поля: id, name, description.
    """
    class Meta:
        model = Location
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]