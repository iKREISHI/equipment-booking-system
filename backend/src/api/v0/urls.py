from rest_framework.routers import DefaultRouter
from api.v0.views.users.login import LoginViewSet
from api.v0.views.users.logout import LogoutViewSet
from api.v0.views.users.registration import RegistrationViewSet
from api.v0.views.users.users import UserAdminViewSet


router = DefaultRouter()
router.register('login', LoginViewSet, basename='login')
router.register('logout', LogoutViewSet, basename='logout')
router.register('registration', RegistrationViewSet, basename='registration')
router.register('users', UserAdminViewSet, basename='users')

urlpatterns = [

] + router.urls