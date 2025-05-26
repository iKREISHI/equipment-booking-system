from rest_framework.routers import DefaultRouter
from api.v0.views.users.login import LoginViewSet
from api.v0.views.users.logout import LogoutViewSet
from api.v0.views.users.registration import RegistrationViewSet
from api.v0.views.users.users import UserAdminViewSet
from api.v0.views.locations.locations import LocationViewSet
from api.v0.views.equipments.inveintiry_equipments_status import InventoryEquipmentStatusViewSet


router = DefaultRouter()
router.register('login', LoginViewSet, basename='login')
router.register('logout', LogoutViewSet, basename='logout')
router.register('registration', RegistrationViewSet, basename='registration')
router.register('users', UserAdminViewSet, basename='users')
router.register('location', LocationViewSet, basename='locations')
router.register('inventory-equipment-status', InventoryEquipmentStatusViewSet, basename='inventory-equipment-status')

urlpatterns = [

] + router.urls