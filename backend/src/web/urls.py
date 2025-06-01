from django.urls import path
from web.views.home_page import HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='view_test'),
]