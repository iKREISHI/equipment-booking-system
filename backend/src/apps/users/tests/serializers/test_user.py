from django.test import TestCase
from apps.users.models import User
from apps.users.serializers import UserSerializer, SmallUserSerializer


class UserSerializerTest(TestCase):
    def setUp(self):
        # создаём пользователя без аватара (avatar=None → serializer выдаст None)
        self.user = User.objects.create_user(
            username='johndoe',
            password='Password123!',
            email='john@example.com',
            last_name='Doe',
            first_name='John',
            patronymic='Jonovich',
            gender='M',
            phone='+1234567890',
            telegram_chat_id='123456',
            avatar=None
        )

    def test_serialization(self):
        """Поля сериализуются корректно и совпадают с атрибутами модели."""
        serializer = UserSerializer(self.user)
        data = serializer.data
        expected_fields = {
            'id', 'username', 'email',
            'last_name', 'first_name', 'patronymic',
            'gender', 'phone', 'telegram_chat_id', 'avatar'
        }
        self.assertEqual(set(data.keys()), expected_fields)
        self.assertEqual(data['id'], self.user.id)
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['last_name'], self.user.last_name)
        self.assertEqual(data['first_name'], self.user.first_name)
