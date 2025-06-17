from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms.inventory_import import InventoryImportForm
from apps.equipments.models.inventory_import import InventoryImport
from apps.equipments.service.inventory_import import run_inventory_import


class InventoryImportPageView(LoginRequiredMixin, View):
    """
    Одна страница: список импортов + модальное окно загрузки + модальные детали.
    GET  → вывести страницу
    POST → принять файл, запустить импорт, показать ту же страницу с обновлённым списком
    """

    template_name = "pages/inventory_equipment/inventory_import_page.html"

    def get_queryset(self, request):
        qs = InventoryImport.objects.order_by("-uploaded_at")
        if not request.user.is_superuser:
            qs = qs.filter(created_by=request.user)
        return qs

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "imports": self.get_queryset(request),
                "form": InventoryImportForm(),
            },
        )

    def post(self, request, *args, **kwargs):
        form = InventoryImportForm(request.POST, request.FILES)
        if form.is_valid():
            imp: InventoryImport = form.save(commit=False)
            imp.created_by = request.user
            imp.save()
            run_inventory_import(imp)  # синхронно

            # хотим, чтобы модальное окно «детали» открывалось сразу после загрузки
            request.session["open_detail_id"] = imp.pk
            return redirect(request.path)  # PRG-паттерн

        # если форма невалидна — показываем ошибки в том же модальном окне
        return render(
            request,
            self.template_name,
            {
                "imports": self.get_queryset(request),
                "form": form,
            },
        )
