import string
from datetime import timedelta
import random
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from apps.users.validators.user_validators import validate_last_name, validate_first_name, validate_patronymic, \
    validate_gender, validate_phone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        if not password:
            raise ValueError('The password must be set')
        try:
            validate_password(password, user=None)
        except ValidationError:
            raise ValueError('The given password must be at least 8 characters long')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username : str, password : str, **extra_fields):
        """
        Create and save a User with the given username and password.
        """
        if not username:
            raise ValueError('The username must be set')
        if not password:
            raise ValueError('The password must be set')

        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # if not Position.objects.filter(name="Администратор").exists():
        #     raise RuntimeError("Перед созданием суперпользователя необходимо выполнить `make entrypoint`"
        #                        "для создания групп пользователей")

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, **extra_fields)

    def make_random_password(self):
        """
        Генерирует случайный пароль длиной от 10 до 14 символов.
        Включает буквы, цифры и специальные символы.
        """
        length = random.randint(10, 14)  # Генерируем случайную длину пароля
        chars = string.ascii_letters + string.digits  # Символы для пароля
        password = ''.join(random.choice(chars) for _ in range(length))  # Генерация пароля
        return password


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=128,
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name=_("Фамилия"),
        validators=[validate_last_name],
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name=_("Имя"),
        validators=[validate_first_name],
    )
    patronymic = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("Отчество"),
        validators=[validate_patronymic],
    )

    GENDER_CHOICES = [
        ('M', _("Мужской")),
        ('F', _("Женский")),
        #('U', _("Не указан")),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        #default='U',
        verbose_name=_("Пол"),
        validators=[validate_gender],
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=128,
        error_messages={
            'required': 'Пожалуйста, заполните поле пароля.',
        }
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_("Почта")
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Номер телефона"),
        validators=[validate_phone],
    )
    telegram_chat_id = models.CharField( # we need this?
        null=True,
        blank=True,
        verbose_name='Чат ID телеграмма для отправки уведомлений',
        max_length=255,
    )
    date_joined = models.DateTimeField(
        verbose_name='Дата создания аккаунта',
        default=timezone.now
    )
    is_staff = models.BooleanField(
        _('staff'), default=False
    )
    is_active = models.BooleanField(
        _('active'), default=True
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='avatars/',
        null=True, blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # Дополнительные обязательные поля можно указать здесь

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        parts = [self.last_name, self.first_name, self.patronymic]
        return " ".join(filter(None, parts))

    def get_short_name(self):
        parts = [self.last_name, self.first_name[0] if self.first_name else "", self.patronymic[0] if self.patronymic else ""]
        return " ".join(filter(None, parts))

    def __str__(self):
        parts = [self.last_name, self.first_name[0] if self.first_name else "",
                 self.patronymic[0] if self.patronymic else ""]
        return " ".join(filter(None, parts))