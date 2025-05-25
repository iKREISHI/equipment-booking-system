from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from apps.users.models import User
from apps.users.validators.user_validators import (
    validate_last_name, validate_first_name, validate_patronymic,
    validate_gender, validate_phone, validate_photo_size
)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label="Подтверждение пароля"
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password2',
            'last_name',
            'first_name',
            'patronymic',
            'gender',
            'email',
            'phone',
            'avatar',
        )
        allow_null = True
        extra_kwargs = {
            'last_name': {'validators': [validate_last_name]},
            'first_name': {'validators': [validate_first_name]},
            'patronymic': {'validators': [validate_patronymic]},
            'gender': {'validators': [validate_gender]},
            'phone': {'validators': [validate_phone]},
            # # удаляем avatar-здесь, будем валидировать через метод ниже
            # 'avatar': {'validators': [validate_photo_size]}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': "Пароли не совпадают."
            })
        return attrs

    def validate_avatar(self, value):
        # вызываем ваш низкоуровневый валидатор
        try:
            validate_photo_size(value)
        except DjangoValidationError as e:
            # оборачиваем в DRF-ошибку
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        # убираем временные поля
        validated_data.pop('password2')
        password = validated_data.pop('password')

        # теперь явно вынимаем username
        username = validated_data.pop('username')

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                **validated_data
            )
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return user
