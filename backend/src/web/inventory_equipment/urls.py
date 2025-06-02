from django.urls import path
from web.inventory_equipment.views.location import LocationListView, LocationCreateView, LocationUpdateView, \
    LocationDeleteView

urlpatterns = [
    path('', LocationListView.as_view(), name='location_list'),
    path('create/', LocationCreateView.as_view(), name='location_create'),
    path('update/<int:pk>/', LocationUpdateView.as_view(), name='location_update'),
    path('delete/<int:pk>/', LocationDeleteView.as_view(), name='location_delete'),
]

