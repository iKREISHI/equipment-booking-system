from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.reservations.models import Reservation
from web.reservation.forms.reservation import ReservationForm


class ReservationListView(LoginRequiredMixin, ListView):
    """
    Отображает список бронирований (с пагинацией).
    В контексте кладёт:
      - create_form: пустая форма для модалки «Добавить»
      - у каждого reservation добавляет атрибут update_form (instance-форма) для модалки «Редактировать»
    При этом выводятся только записи, у которых assigned_by не равен null.
    """
    model = Reservation
    template_name = "pages/reservation/reservation.html"
    context_object_name = "reservations"
    paginate_by = 10

    def get_queryset(self):
        # фильтруем, чтобы остались только те Reservation, у которых assigned_by не null
        if self.request.user.is_superuser:
            return super().get_queryset().filter(assigned_by__isnull=False)
        else:
            return super().get_queryset().filter(assigned_by__isnull=False, renter__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Пустая форма для создания новой аренды
        context["create_form"] = ReservationForm()
        # Для каждого reservation в списке задаём форму-инстанс для редактирования
        for res in context["page_obj"].object_list:
            res.update_form = ReservationForm(instance=res)
        return context



class ReservationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Обработка POST-запроса «Добавить аренду».
    При GET сразу редиректим на список.
    """
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservation_list")

    def get_permission_required(self):
        app_label = self.model._meta.app_label       # "reservations"
        model_name = self.model._meta.model_name     # "reservation"
        return (f"{app_label}.add_{model_name}",)

    def get(self, request, *args, **kwargs):
        # При попытке напрямую зайти на URL create/ — возвращаем на список
        return redirect(self.success_url)

    def form_valid(self, form):
        # перед сохранием заполняем renter и assigned_by текущим user
        reservation = form.save(commit=False)
        reservation.renter = self.request.user
        if (self.request.user.is_superuser
                or self.request.user.has_perm("reservation.change_reservation")):
            reservation.assigned_by = self.request.user
        reservation.save()
        return super().form_valid(form)


class ReservationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    При любом GET-запросе сразу редиректим на список.
    Только POST (submit формы из модалки) обрабатываем как Update.
    """
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservation_list")

    def get_permission_required(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return (f"{app_label}.change_{model_name}",)

    def dispatch(self, request, *args, **kwargs):
        # Если метод GET, сразу возвращаем редирект на список
        if request.method.upper() == "GET":
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class ReservationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Обработка POST-запроса «Удалить аренду».
    При GET сразу редиректим на список.
    """
    model = Reservation
    success_url = reverse_lazy("reservation_list")

    def get_permission_required(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return (f"{app_label}.delete_{model_name}",)

    def get(self, request, *args, **kwargs):
        # При переходе по delete/<pk>/ возвращаемся на список
        return redirect(self.success_url)
