import io
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from apps.users.serializers import UserRegistrationSerializer
from apps.users.models import User


class UserRegistrationSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'password': 'StrongPass123',
            'password2': 'StrongPass123',
            'last_name': 'Иванов',
            'first_name': 'Иван',
            'patronymic': 'Иванович',
            'gender': 'M',
            'email': 'test@example.com',
            'phone': '+71234567890',
        }

    def test_valid_data_creates_user(self):
        serializer = UserRegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()

        # Проверяем, что юзер создан в базе
        self.assertIsInstance(user, User)
        # Пароль правильно захеширован
        self.assertTrue(user.check_password(self.valid_data['password']))
        # Поля совпадают
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertEqual(user.last_name, self.valid_data['last_name'])
        self.assertEqual(user.gender, self.valid_data['gender'])

    def test_password_mismatch(self):
        data = self.valid_data.copy()
        data['password2'] = 'Different123'
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password2', serializer.errors)
        self.assertEqual(
            serializer.errors['password2'][0],
            "Пароли не совпадают."
        )

    def test_invalid_last_name(self):
        data = self.valid_data.copy()
        data['last_name'] = 'Ivan123'
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('last_name', serializer.errors)

    def test_invalid_phone(self):
        data = self.valid_data.copy()
        data['phone'] = '123ab'
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('phone', serializer.errors)

    def test_invalid_gender(self):
        data = self.valid_data.copy()
        data['gender'] = 'X'
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('gender', serializer.errors)

    def test_optional_patronymic(self):
        data = self.valid_data.copy()
        data.pop('patronymic')
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

# TODO: написать нормально тест проверки размера фото аватара профиля
    # def test_avatar_size_validation(self):
    #     # создаём файл чуть больше 2 МБ
    #     large_content = b'a' * (2 * 1024 * 1024 + 1)
    #     avatar = SimpleUploadedFile('avatar.jpg', large_content, content_type='image/jpeg')
    #     data = self.valid_data.copy()
    #     data['avatar'] = avatar
    #
    #     serializer = UserRegistrationSerializer(data=data)
    #     self.assertFalse(serializer.is_valid())
    #     self.assertIn('avatar', serializer.errors)
    #     # Можно проверить часть сообщения
    #     self.assertTrue(any("Размер фото" in msg for msg in serializer.errors['avatar']))
