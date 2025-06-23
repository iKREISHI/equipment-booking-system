from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.reservations.models import Reservation
from apps.equipments.models import InventoryEquipmentStatus
from web.reservation.forms.reservation import ReservationForm
from config import settings

ISO_FMT = "%Y-%m-%dT%H:%M"


class ReservationListView(LoginRequiredMixin,
                           PermissionRequiredMixin,
                           ListView):
    """
    Список бронирований с модальными формами «Добавить / Редактировать».
    Отображаются только записи, у которых assigned_by не null.
    """
    model = Reservation
    template_name = "pages/reservation/reservation.html"
    context_object_name = "reservations"
    paginate_by = 10

    # --- права -----------------------------------------------------------------
    def get_permission_required(self):
        meta = self.model._meta
        return (
            f"{meta.app_label}.view_{meta.model_name}",
            # f"{meta.app_label}.change_{meta.model_name}",
            f"{meta.app_label}.add_{meta.model_name}",
            # f"{meta.app_label}.delete_{meta.model_name}",
        )

    # --- утилита для ISO-формата -----------------------------------------------
    @staticmethod
    def _to_iso(dt):
        """YYYY-MM-DDTHH:MM для <input type="datetime-local">."""
        if dt is None:
            return ""
        if settings.USE_TZ and timezone.is_aware(dt):
            dt = timezone.localtime(dt)
        return dt.strftime(ISO_FMT)

    # --- выборка ---------------------------------------------------------------
    def get_queryset(self):
        qs = (super().get_queryset().filter(assigned_by__isnull=False)
              .exclude(status=3))
        if self.request.user.is_superuser:
            return qs
        return qs.filter(renter_id=self.request.user.id)

    # --- контекст --------------------------------------------------------------
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["create_form"] = ReservationForm()
        for r in ctx["page_obj"].object_list:
            r.update_form = ReservationForm(
                instance=r,
                initial={
                    "start_time": self._to_iso(getattr(r, "start_time", None)),
                    "end_time": self._to_iso(getattr(r, "end_time", None)),
                },
            )
        return ctx


# ------------------------------------------------------------------------------
# CREATE
# ------------------------------------------------------------------------------

class ReservationCreateView(LoginRequiredMixin,
                             PermissionRequiredMixin,
                             CreateView):
    """POST из модалки «Добавить бронирование». GET → список."""
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservation_list")

    def get_permission_required(self):
        meta = self.model._meta
        return (f"{meta.app_label}.add_{meta.model_name}",)

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def form_valid(self, form):
        reservation = form.save(commit=False)
        reservation.renter = self.request.user
        if (self.request.user.is_superuser or
                self.request.user.has_perm("reservations.change_reservation")):
            reservation.assigned_by = self.request.user
            reservation.status = 2
        reservation.save()
        equipment = reservation.equipment.status

        status, _ = InventoryEquipmentStatus.objects.get_or_create(
            name="Забронировано"
        )
        if equipment:
            equipment.status = status
            equipment.save()
        messages.success(self.request, "Бронирование успешно создано.")
        return super().form_valid(form)

    def form_invalid(self, form):
        list_view = ReservationListView()
        list_view.request = self.request
        context = list_view.get_context_data()
        context["create_form"] = form
        context["show_create_modal"] = True
        return render(self.request, list_view.template_name, context)



# ------------------------------------------------------------------------------
# UPDATE
# ------------------------------------------------------------------------------

class ReservationUpdateView(LoginRequiredMixin,
                             PermissionRequiredMixin,
                             UpdateView):
    """Редактирование бронирования. GET → список, POST — апдейт."""
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservation_list")

    def get_permission_required(self):
        meta = self.model._meta
        return (f"{meta.app_label}.change_{meta.model_name}",)

    def dispatch(self, request, *args, **kwargs):
        if request.method.upper() == "GET":
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        reservation = form.save()
        # ReservationCreateView._update_equipment_status(reservation)
        if form.cleaned_data["actual_return_time"]:
            reservation.status = 3
            equipment = reservation.equipment
            status, _ = InventoryEquipmentStatus.objects.get_or_create(
                name="Доступно"
            )
            if equipment:
                equipment.status = status
                equipment.save()
        messages.success(self.request, "Бронирование обновлено.")
        return super().form_valid(form)

    def form_invalid(self, form):
        list_view = ReservationListView()
        list_view.request = self.request
        context = list_view.get_context_data()
        # Подставляем проблемную форму в соответствующую mod-форму
        context["update_error_id"] = self.kwargs["pk"]
        context[f"update_form_{self.kwargs['pk']}"] = form
        return render(self.request, list_view.template_name, context)


# ------------------------------------------------------------------------------
# DELETE
# ------------------------------------------------------------------------------

class ReservationDeleteView(LoginRequiredMixin,
                             PermissionRequiredMixin,
                             DeleteView):
    """POST «Удалить бронирование». Перед удалением меняем статус оборудования."""
    model = Reservation
    success_url = reverse_lazy("reservation_list")

    def get_permission_required(self):
        meta = self.model._meta
        return (f"{meta.app_label}.delete_{meta.model_name}",)

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            self.object = self.get_object()
            equipment = self.object.equipment

            available_status, _ = InventoryEquipmentStatus.objects.get_or_create(
                name="Доступно"
            )
            if equipment:
                equipment.status = available_status
                equipment.save(update_fields=["status"])

            messages.success(request, "Бронирование удалено.")
            return super().post(request, *args, **kwargs)
