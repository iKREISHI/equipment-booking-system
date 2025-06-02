from django.urls import path
from django.contrib.auth import views
from web.users.views.registration import RegistrationView


users_urls = [
    path("login/", views.LoginView.as_view(
        template_name="pages/auth/login.html",
        success_url="/web",
    ), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path('registration', RegistrationView.as_view(), name='registration'),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name='user/change_password.html',
            success_url='/users/password_changed/'
        ),
        name="password_change"
    ),
    path(
        "password_changed/",
        views.PasswordChangeDoneView.as_view(
            template_name='user/password_changed.html',
        ),
        name="password_changed",
    ),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]