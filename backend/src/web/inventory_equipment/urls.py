from django.urls import path

from web.inventory_equipment.views.inventory_import import InventoryImportPageView
from web.inventory_equipment.views.location import LocationListView, LocationCreateView, LocationUpdateView, \
    LocationDeleteView

from web.inventory_equipment.views.inventory_equipment import (
    InventoryEquipmentListView,
    InventoryEquipmentUpdateView,
    InventoryEquipmentDeleteView,
    InventoryEquipmentCreateView
)

urlpatterns = [
    path('location-list', LocationListView.as_view(), name='location_list'),
    path('location-create/', LocationCreateView.as_view(), name='location_create'),
    path('location-update/<int:pk>/', LocationUpdateView.as_view(), name='location_update'),
    path('location-delete/<int:pk>/', LocationDeleteView.as_view(), name='location_delete'),

    # inventory equipment
    path('inventory-list', InventoryEquipmentListView.as_view(), name='inventory_list'),
    path('inventory-create/', InventoryEquipmentCreateView.as_view(), name='inventory_create'),
    path('inventory-update/<int:pk>/', InventoryEquipmentUpdateView.as_view(), name='inventory_update'),
    path('inventory-delete/<int:pk>/', InventoryEquipmentDeleteView.as_view(), name='inventory_delete'),
    path("imports/", InventoryImportPageView.as_view(), name="inventory-import-page"),
]

