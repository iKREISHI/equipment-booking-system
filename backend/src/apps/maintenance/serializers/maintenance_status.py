from rest_framework import serializers
from apps.maintenance.models import MaintenanceStatus

class MaintenanceStatusSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели MaintenanceStatus.
    Позволяет получать и обновлять поля name и description.
    """

    class Meta:
        model = MaintenanceStatus
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)
        # extra_kwargs = {
        #     'name': {'required': True, 'allow_blank': False},
        #     'description': {'required': False, 'allow_blank': True},
        # }
