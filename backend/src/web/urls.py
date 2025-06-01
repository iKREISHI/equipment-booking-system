from django.urls import path
from web.views.view_test import ViewTest

urlpatterns = [
    path('', ViewTest.as_view(), name='view_test'),
]