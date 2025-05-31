from rest_framework.routers import DefaultRouter

from api.v0.views.maintenance.maintenance import MaintenanceViewSet
from api.v0.views.maintenance.maintenance_status import MaintenanceStatusViewSet
from api.v0.views.reservations.reservations import ReservationViewSet
from api.v0.views.users.login import LoginViewSet
from api.v0.views.users.logout import LogoutViewSet
from api.v0.views.users.registration import RegistrationViewSet
from api.v0.views.users.users import UserAdminViewSet
from api.v0.views.locations.locations import LocationViewSet
from api.v0.views.equipments.inveintiry_equipments_status import InventoryEquipmentStatusViewSet
from api.v0.views.equipments.inventory_equipment import InventoryEquipmentViewSet


router = DefaultRouter()
router.register('login', LoginViewSet, basename='login')
router.register('logout', LogoutViewSet, basename='logout')
router.register('registration', RegistrationViewSet, basename='registration')
router.register('users', UserAdminViewSet, basename='users')
router.register('location', LocationViewSet, basename='locations')
router.register('inventory-equipment-status', InventoryEquipmentStatusViewSet, basename='inventory-equipment-status')
router.register('inventory-equipment', InventoryEquipmentViewSet, basename='inventory-equipment')
router.register(r"reservation", ReservationViewSet, basename="reservation")
router.register(r'maintenance-status', MaintenanceStatusViewSet, basename='maintenance-status')
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')

urlpatterns = [

] + router.urls