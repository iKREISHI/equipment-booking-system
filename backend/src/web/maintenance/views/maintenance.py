from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.equipments.models import InventoryEquipmentStatus
from apps.maintenance.models import Maintenance
from web.maintenance.forms.maintenance import MaintenanceForm


class MaintenanceListView(LoginRequiredMixin, ListView):
    """
    Отображает список проверок/обслуживаний оборудования (с пагинацией).
    В контексте кладёт:
      - create_form: пустая форма для модалки «Добавить»
      - у каждого maintenance добавляет атрибут update_form (instance-форма) для модалки «Редактировать»
    Выводятся только записи, у которых assigned_by не равен null.
    """
    model = Maintenance
    template_name = "pages/maintenance/maintenance.html"
    context_object_name = "maintenances"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().filter(assigned_by__isnull=False)
        if self.request.user.is_superuser:
            return qs
        return qs.filter(reporter_by_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = MaintenanceForm()
        for m in context["page_obj"].object_list:
            m.update_form = MaintenanceForm(instance=m)
        return context


class MaintenanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Обработка POST-запроса «Добавить обслуживание».
    При GET сразу редиректим на список.
    """
    model = Maintenance
    form_class = MaintenanceForm
    success_url = reverse_lazy("maintenance_list")

    def get_permission_required(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return (f"{app_label}.add_{model_name}",)

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def form_valid(self, form):
        maintenance = form.save(commit=False)
        maintenance.reporter_by = self.request.user
        # если суперпользователь или есть право менять, сразу назначаем проверяющего
        if (self.request.user.is_superuser
                or self.request.user.has_perm('maintenance.change_maintenance')):
            maintenance.assigned_by = self.request.user
        maintenance.save()
        equipment = maintenance.equipment
        if equipment and maintenance.status.name in [
            "В ожидании работы", "В процессе", "Запланировано",
            "Приостановлено"
        ]:
            equipment.status = InventoryEquipmentStatus.objects.filter(name="На тех.обслуживании").first()
            equipment.save()

        if equipment and maintenance.status.name == "Завершено":
            equipment.status = InventoryEquipmentStatus.objects.filter(name="Доступно").first()
            equipment.save()

        if equipment and maintenance.status.name in ["Требуется ремонт"]:
            equipment.status = InventoryEquipmentStatus.objects.filter(name="Не доступно").first()
            equipment.save()


        return super().form_valid(form)

    def form_invalid(self, form):
        list_view = MaintenanceListView()
        list_view.request = self.request
        context = list_view.get_context_data()
        context['create_form'] = form
        context['show_create_modal'] = True
        return render(self.request, list_view.template_name, context)


class MaintenanceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Обработка POST-запроса «Редактировать обслуживание».
    При GET сразу редиректим на список.
    """
    model = Maintenance
    form_class = MaintenanceForm
    success_url = reverse_lazy("maintenance_list")

    def get_permission_required(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return (f"{app_label}.change_{model_name}",)

    def dispatch(self, request, *args, **kwargs):
        if request.method.upper() == "GET":
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class MaintenanceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Обработка POST-запроса «Удалить обслуживание».
    При GET сразу редиректим на список.
    """
    model = Maintenance
    success_url = reverse_lazy("maintenance_list")

    def get_permission_required(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return (f"{app_label}.delete_{model_name}",)

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)
