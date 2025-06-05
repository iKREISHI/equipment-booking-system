from django import forms
from apps.reservations.models import Reservation
from apps.equipments.models.inventory_equipment import InventoryEquipment


class ReservationForm(forms.ModelForm):
    equipment = forms.ModelChoiceField(
        # По умолчанию — только доступное оборудование
        queryset=InventoryEquipment.objects.filter(status__name="Доступно"),
        label="Оборудование*",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    end_time = forms.DateTimeField(
        label="Время окончания*",
        widget=forms.DateTimeInput(attrs={
            "class": "form-control",
            "type": "datetime-local"
        }),
        required=True,
    )
    actual_return_time = forms.DateTimeField(
        label="Фактическое время возврата",
        widget=forms.DateTimeInput(attrs={
            "class": "form-control",
            "type": "datetime-local"
        }),
        required=False,
    )
    location = forms.CharField(
        label="Расположение*",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
        }),
        required=True,
    )
    description = forms.CharField(
        label="Описание аренды",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Дополнительные детали (необязательно)"
        }),
        required=False,
    )

    class Meta:
        model = Reservation
        fields = [
            "equipment",
            "end_time",
            "actual_return_time",
            "location",
            "description",
        ]
        labels = {
            "equipment": "Оборудование*",
            "end_time": "Время окончания*",
            "actual_return_time": "Фактическое время возврата",
            "location": "Расположение*",
            "description": "Описание аренды",
        }
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        """
        Если это форма для редактирования (instance.pk есть),
        добавляем в queryset текущее оборудование, даже если его статус
        перестал быть "Доступно".
        """
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            current_eq = self.instance.equipment
            # Берём все «Доступные» + текущее оборудование (чтобы форма не сломалась)
            qs = InventoryEquipment.objects.filter(status__name="Доступно") \
                 | InventoryEquipment.objects.filter(pk=current_eq.pk)
            self.fields["equipment"].queryset = qs.distinct()
        else:
            # Обычное создание: только "Доступные"
            self.fields["equipment"].queryset = InventoryEquipment.objects.filter(status__name="Доступно")
