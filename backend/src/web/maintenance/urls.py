from django.urls import path

from web.maintenance.views.maintenance import MaintenanceListView, MaintenanceCreateView, MaintenanceUpdateView, \
    MaintenanceDeleteView

urlpatterns = [
    path('', MaintenanceListView.as_view(), name='maintenance_list'),
    # Добавить обслуживание
    path('create/', MaintenanceCreateView.as_view(), name='maintenance_create'),
    # Редактировать обслуживание
    path('update/<int:pk>/', MaintenanceUpdateView.as_view(), name='maintenance_update'),
    # Удалить обслуживание
    path('delete/<int:pk>/', MaintenanceDeleteView.as_view(), name='maintenance_delete'),

]