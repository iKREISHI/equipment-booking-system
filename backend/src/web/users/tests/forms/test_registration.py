from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from captcha.models import CaptchaStore
from unittest.mock import patch
from django.http import HttpResponse

from web.users.forms.registration import UserRegisterForm
from apps.users.models.users import User

UserModel = get_user_model()


class UserRegisterFormTest(TestCase):
    def setUp(self):
        # Создаём пользователя для проверки дублирования
        UserModel.objects.create_user(
            username="existing",
            password="ExistingPassword1",
            last_name="Петров",
            first_name="Пётр",
            gender="M",
            email="exist@example.com",
            phone="+79990001122"
        )

    def _get_captcha(self):
        """
        Генерирует валидные пары (hashkey, challenge) для тестирования CaptchaField.
        Возвращает словарь вида {
            'captcha_0': hashkey,
            'captcha_1': challenge
        }
        """
        key = CaptchaStore.generate_key()
        challenge = CaptchaStore.objects.get(hashkey=key).challenge
        return {"captcha_0": key, "captcha_1": challenge}

    def test_form_valid_data(self):
        """
        Данные корректны, пользователь не дублируется.
        Форма должна быть валидна и создать нового пользователя.
        """
        captcha_data = self._get_captcha()
        valid_data = {
            "username": "newuser",
            "last_name": "Иванов",
            "first_name": "Иван",
            "patronymic": "Иванович",
            "gender": "M",
            "email": "newuser@example.com",
            "phone": "+79991234567",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
            **captcha_data
        }
        form = UserRegisterForm(data=valid_data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_json())

        user = form.save()
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, valid_data["username"])
        self.assertEqual(user.last_name, valid_data["last_name"])
        self.assertEqual(user.first_name, valid_data["first_name"])
        self.assertEqual(user.patronymic, valid_data["patronymic"])
        self.assertEqual(user.gender, valid_data["gender"])
        self.assertEqual(user.email, valid_data["email"])
        self.assertEqual(user.phone, valid_data["phone"])
        self.assertTrue(user.check_password(valid_data["password1"]))

    def test_form_password_mismatch(self):
        """
        Если password1 и password2 не совпадают, форма невалидна, ключ 'password2' содержит ошибку.
        """
        captcha_data = self._get_captcha()
        data = {
            "username": "anotheruser",
            "last_name": "Сидоров",
            "first_name": "Сидор",
            "patronymic": "",
            "gender": "M",
            "email": "another@example.com",
            "phone": "+79992345678",
            "password1": "PasswordOne123",
            "password2": "Different123",
            **captcha_data
        }
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        # Проверяем, что ошибка есть в password2
        self.assertIn("password2", form.errors)
        # Сообщение об ошибке password mismatch будет содержать слово "не совпадают"
        self.assertIn("не совпадают", form.errors["password2"][0])

    def test_form_username_duplicate(self):
        """
        Повтор существующего username ("existing") даёт ошибку в поле 'username'.
        """
        captcha_data = self._get_captcha()
        data = {
            "username": "existing",
            "last_name": "Новый",
            "first_name": "Пользователь",
            "patronymic": "",
            "gender": "U",
            "email": "unique@example.com",
            "phone": "+79993456789",
            "password1": "UniquePassword1",
            "password2": "UniquePassword1",
            **captcha_data
        }
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        # Django по умолчанию выдаёт сообщение вида "Пользователь с таким Имя пользователя уже существует."
        self.assertIn("существует", form.errors["username"][0])

    def test_form_email_duplicate(self):
        """
        Повтор существующего email ("exist@example.com") даёт ошибку в поле 'email'.
        """
        captcha_data = self._get_captcha()
        data = {
            "username": "uniqueuser",
            "last_name": "Новый",
            "first_name": "Пользователь",
            "patronymic": "",
            "gender": "F",
            "email": "exist@example.com",
            "phone": "+79994567890",
            "password1": "AnotherPass123",
            "password2": "AnotherPass123",
            **captcha_data
        }
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        # Проверяем, что в сообщении есть фраза "уже зарегистрирован"
        self.assertIn("уже зарегистрирован", form.errors["email"][0])

    def test_form_phone_duplicate(self):
        """
        Повтор существующего phone ("+79990001122") даёт ошибку в поле 'phone'.
        """
        captcha_data = self._get_captcha()
        data = {
            "username": "uniqueuser2",
            "last_name": "Новый",
            "first_name": "Пользователь",
            "patronymic": "",
            "gender": "U",
            "email": "unique2@example.com",
            "phone": "+79990001122",
            "password1": "AnotherPass456",
            "password2": "AnotherPass456",
            **captcha_data
        }
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)
        self.assertIn("уже зарегистрирован", form.errors["phone"][0])

    def test_form_missing_required_field(self):
        """
        Если не передан обязательный last_name, форма невалидна, ключ 'last_name' содержит ошибку.
        """
        captcha_data = self._get_captcha()
        data = {
            "username": "userwithoutlastname",
            # last_name отсутствует
            "first_name": "БезФамилии",
            "patronymic": "",
            "gender": "U",
            "email": "nolast@example.com",
            "phone": "+79995678901",
            "password1": "NoLastPass123",
            "password2": "NoLastPass123",
            **captcha_data
        }
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)
        # Стандартное сообщение об обязательном поле — "Обязательное поле."
        self.assertIn("Обязательное поле", form.errors["last_name"][0])


@patch('web.users.views.registration.render', return_value=HttpResponse())
class RegistrationViewTest(TestCase):
    def setUp(self):
        self.url = reverse("registration")  # имя URL регистрации в urls.py
        # Убедимся, что пользователя с таким username нет
        self.assertFalse(UserModel.objects.filter(username="viewuser").exists())

    def _get_captcha(self):
        key = CaptchaStore.generate_key()
        challenge = CaptchaStore.objects.get(hashkey=key).challenge
        return {"captcha_0": key, "captcha_1": challenge}

    def test_get_registration_page(self, mock_render):
        """
        GET-запрос к странице регистрации должен вернуть 200 и обеспечить наличие
        формы (класса) в контексте.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Поскольку для GET мы передаём класс формы, проверяем, что context["form"] == UserRegisterForm
        _, _, context = mock_render.call_args[0]
        self.assertEqual(context.get("form"), UserRegisterForm)

    def test_post_valid_data_creates_and_logs_in_user(self, mock_render):
        """
        POST с правильными данными должен создать пользователя, выполнить login
        и вернуть редирект (302) на 'homepage'.
        """
        captcha_data = self._get_captcha()
        valid_data = {
            "username": "viewuser",
            "last_name": "Тестов",
            "first_name": "Вью",
            "patronymic": "Польз",
            "gender": "F",
            "email": "viewuser@example.com",
            "phone": "+79996789012",
            "password1": "ViewPass123",
            "password2": "ViewPass123",
            **captcha_data
        }
        response = self.client.post(self.url, data=valid_data)
        # Проверяем, что статус 302 и Location соответствует reverse("homepage")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("homepage"))

        # Проверяем, что пользователь создан
        user = UserModel.objects.filter(username="viewuser").first()
        self.assertIsNotNone(user)

        # Проверяем, что после выполнения POST пользователь залогинен (session содержит ключ)
        session = self.client.session
        self.assertIn("_auth_user_id", session)

    def test_post_invalid_data_shows_errors(self, mock_render):
        """
        POST с неверными данными (несовпадающие пароли или неверный captcha)
        должен вернуть 200, форму с ошибками, и не создавать пользователя.
        """
        captcha_data = self._get_captcha()
        invalid_data = {
            "username": "viewuser2",
            "last_name": "Ошибка",
            "first_name": "Вью",
            "patronymic": "",
            "gender": "M",
            "email": "error@example.com",
            "phone": "+79997890123",
            "password1": "Pass123",
            "password2": "Mismatch123",
            # Передадим неправильный ответ для captcha
            "captcha_0": captcha_data["captcha_0"],
            "captcha_1": "WRONG",
        }
        response = self.client.post(self.url, data=invalid_data)
        # Форма с ошибками: статус 200
        self.assertEqual(response.status_code, 200)

        # Проверяем, что render был вызван с формой, содержащей ошибки
        _, _, context = mock_render.call_args[0]
        form = context.get("form")
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
        self.assertIn("captcha", form.errors)

        # Пользователь не создан
        self.assertFalse(UserModel.objects.filter(username="viewuser2").exists())
