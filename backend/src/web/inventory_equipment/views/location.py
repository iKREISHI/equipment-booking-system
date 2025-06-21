from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from apps.locations.models import Location
from web.inventory_equipment.forms.location import LocationForm


class LocationListView(LoginRequiredMixin, ListView):
    """
    Отображает список локаций с пагинацией.
    """
    model = Location
    template_name = "pages/inventory_equipment/location.html"
    context_object_name = "locations"
    paginate_by = 10  # количество элементов на странице


class LocationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Обрабатывает создание новой локации.
    Требует права add_location.
    """
    model = Location
    form_class = LocationForm
    # после успешного создания — возвращаемся к списку
    success_url = reverse_lazy("location_list")

    def get_permission_required(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return (f"{app_label}.add_{model_name}",)

    # При попытке GET-запроса на этот URL можно либо
    # перенаправить на список, либо показать отдельную страницу.
    # В нашем случае модальное окно открывается на странице списка,
    # поэтому GET-метод для CreateView не предполагается.


class LocationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Обрабатывает редактирование существующей локации.
    Требует права change_location.
    """
    model = Location
    form_class = LocationForm
    success_url = reverse_lazy("location_list")

    def get_permission_required(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return (f"{app_label}.change_{model_name}",)


class LocationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Обрабатывает удаление локации.
    Требует права delete_location.
    """
    model = Location
    success_url = reverse_lazy("location_list")

    def get_permission_required(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return (f"{app_label}.delete_{model_name}",)
