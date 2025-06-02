from django.urls import path, include
from web.views.home_page import HomePage
from .users.urls import users_urls

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('location', include('web.inventory_equipment.urls')),
] + users_urls
