from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from apps.reservations.models import Reservation
from web.reservation.forms.approve import RejectReasonForm


class ReservationPendingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Страница «Ожидающие одобрения» (assigned_by IS NULL, status=0).
    """
    model = Reservation
    template_name = "pages/reservation/reservation_pending.html"
    context_object_name = "reservations"
    paginate_by = 20  # можно изменить

    def get_permission_required(self):
        # Требуем право change_reservation (можно сделать кастомное can_approve_reservation)
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return (f"{app_label}.change_{model_name}",)

    def get_queryset(self):
        # Только те, у которых еще не назначен assigned_by и status == 0
        return super().get_queryset().filter(assigned_by__isnull=True, status=0).order_by("start_time")


class ApproveReservationView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Обработка нажатия «Approve» (ставим assigned_by=current user, status=1).
    """
    def get_permission_required(self):
        return ("reservations.change_reservation",)

    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, assigned_by__isnull=True, status=0)
        reservation.assigned_by = request.user
        reservation.status = 1  # Одобрен
        reservation.status_response = ""  # Очищаем, чтобы не было старых текстов
        reservation.save()
        return redirect(reverse_lazy("reservation_pending"))


class RejectReservationView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Обработка нажатия «Reject» (ставим assigned_by=current user, status=0, сохраняем reason).
    """
    def get_permission_required(self):
        return ("reservations.change_reservation",)

    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, assigned_by__isnull=True, status=0)
        form = RejectReasonForm(request.POST)
        if form.is_valid():
            reservation.assigned_by = request.user
            reservation.status = 0  # Отклонено
            reservation.status_response = form.cleaned_data["status_response"]
            reservation.save()
        return redirect(reverse_lazy("reservation_pending"))