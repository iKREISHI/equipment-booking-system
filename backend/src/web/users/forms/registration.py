from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from apps.users.models.users import User
from captcha.fields import CaptchaField, CaptchaTextInput


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя*",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите имя пользователя"
        }),
        required=True
    )

    last_name = forms.CharField(
        label="Фамилия*",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите фамилию"
        }),
        required=True
    )

    first_name = forms.CharField(
        label="Имя*",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите имя"
        }),
        required=True
    )

    patronymic = forms.CharField(
        label="Отчество",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите отчество"
        }),
        required=False
    )

    gender = forms.ChoiceField(
        label="Пол*",
        choices=User.GENDER_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-select"
        }),
        required=True
    )

    email = forms.EmailField(
        label="Email*",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Введите email"
        }),
        required=True
    )

    phone = forms.CharField(
        label="Телефон*",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите номер телефона"
        }),
        required=True
    )

    avatar = forms.ImageField(
        label="Аватар",
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control"
        }),
        required=False
    )

    captcha = CaptchaField(
        label="Подтвердите проверку*",
        widget=CaptchaTextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите текст с картинки"
        }),
        error_messages={"invalid": _("Неверный текст с картинки.")},
        required=True
    )

    error_messages = {
        "password_mismatch": _("Введённые пароли не совпадают."),
    }
    password1 = forms.CharField(
        label="Пароль*",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "class": "form-control",
            "placeholder": "Введите пароль"
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля*",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "class": "form-control",
            "placeholder": "Подтвердите пароль"
        }),
        help_text=_("Введите тот же пароль ещё раз для подтверждения."),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "last_name",
            "first_name",
            "patronymic",
            "gender",
            "email",
            "phone",
            "avatar",
            "password1",
            "password2",
            "captcha",
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")

        if username and User.objects.filter(username=username).exists():
            self.add_error("username", f"Пользователь с именем «{username}» уже существует.")

        if email:
            qs_email = User.objects.filter(email=email)
            if qs_email.exists():
                self.add_error("email", f"Пользователь с email «{email}» уже зарегистрирован.")

        if phone:
            qs_phone = User.objects.filter(phone=phone)
            if qs_phone.exists():
                self.add_error("phone", f"Пользователь с номером «{phone}» уже зарегистрирован.")
