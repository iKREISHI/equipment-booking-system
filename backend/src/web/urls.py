from django.urls import path
from web.views.home_page import HomePage
from .users.urls import users_urls

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
] + users_urls