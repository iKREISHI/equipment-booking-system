from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.equipments.models import InventoryEquipment
from web.inventory_equipment.forms.inventory_equipment import InventoryEquipmentForm
from apps.users.models.users import User
from apps.equipments.models.inventory_equipment_status import InventoryEquipmentStatus
from apps.locations.models import Location


class InventoryEquipmentListView(LoginRequiredMixin, ListView):
    """
    Отображает список инвентарного оборудования с пагинацией и модальными формами «Создать» и «Редактировать».
    """
    model = InventoryEquipment
    # Указываем реальный путь к шаблону, где лежит файл inventory_list.html
    template_name = "pages/inventory_equipment/inventory_equipment.html"
    context_object_name = "equipments"
    paginate_by = 10  # количество элементов на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Пустая форма для создания нового оборудования
        context['form'] = InventoryEquipmentForm()

        # Словарь форм для редактирования: { equipment.id: InventoryEquipmentForm(instance=equipment) }
        context['update_forms'] = {
            equip.id: InventoryEquipmentForm(instance=equip)
            for equip in context['page_obj'].object_list
        }

        # Данные для выпадающих списков (users, statuses, locations)
        context['users'] = User.objects.filter(is_active=True)
        context['statuses'] = InventoryEquipmentStatus.objects.all()
        context['locations'] = Location.objects.all()

        return context


class InventoryEquipmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Обрабатывает POST-запрос на создание нового оборудования.
    Требует права add_inventoryequipment.
    """
    model = InventoryEquipment
    form_class = InventoryEquipmentForm
    success_url = reverse_lazy("inventory_list")

    def get_permission_required(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return (f"{app_label}.add_{model_name}",)


class InventoryEquipmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Обрабатывает POST-запрос на редактирование существующего оборудования.
    Требует права change_inventoryequipment.
    """
    model = InventoryEquipment
    form_class = InventoryEquipmentForm
    success_url = reverse_lazy("inventory_list")

    def get_permission_required(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return (f"{app_label}.change_{model_name}",)


class InventoryEquipmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Обрабатывает POST-запрос на удаление оборудования.
    Требует права delete_inventoryequipment.
    """
    model = InventoryEquipment
    success_url = reverse_lazy("inventory_list")

    def get_permission_required(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return (f"{app_label}.delete_{model_name}",)
