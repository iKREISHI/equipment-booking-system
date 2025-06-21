from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.reservations.models import Reservation   # имя модели оставьте своё

class HomePage(LoginRequiredMixin, View):
    template_name = "pages/homepage.html"
    paginate_by   = 10                # элементов на страницу

    def get(self, request):
        qs = (Reservation.objects
            .select_related("equipment")
            .filter(status=2)
            .order_by("start_time"))

        paginator  = Paginator(qs, self.paginate_by)
        page_obj   = paginator.get_page(request.GET.get("page"))

        return render(request, self.template_name, {"page_obj": page_obj})
