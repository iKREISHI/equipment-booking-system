from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'last_name', 'first_name', 'patronymic',
            'gender', 'phone', 'telegram_chat_id',
            'avatar'
        ]
        read_only_fields = ['id']


class SmallUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',]
        read_only_fields = ['id']

class SetActiveSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True)