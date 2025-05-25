from rest_framework.routers import DefaultRouter
from api.v0.views.users.login import LoginViewSet
from api.v0.views.users.logout import LogoutViewSet


router = DefaultRouter()
router.register('login', LoginViewSet, basename='login')
router.register('logout', LogoutViewSet, basename='logout')
urlpatterns = [

] + router.urls