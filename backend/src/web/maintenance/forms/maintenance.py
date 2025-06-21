from django import forms
from apps.maintenance.models import Maintenance
from apps.equipments.models.inventory_equipment import InventoryEquipment
from apps.maintenance.models.maintenance_status import MaintenanceStatus


class MaintenanceForm(forms.ModelForm):
    equipment = forms.ModelChoiceField(
        # По умолчанию — только доступное оборудование
        queryset=InventoryEquipment.objects.exclude(status__name="В аренде"),
        label="Оборудование*",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    start_time = forms.DateTimeField(
        label="Дата и время начала обслуживания*",
        widget=forms.DateTimeInput(attrs={
            "class": "form-control",
            "type": "datetime-local",
        }),
        required=True,
    )
    end_time = forms.DateTimeField(
        label="Дата и время конца обслуживания*",
        widget=forms.DateTimeInput(attrs={
            "class": "form-control",
            "type": "datetime-local",
        }),
        required=True,
    )
    status = forms.ModelChoiceField(
        queryset=MaintenanceStatus.objects.all(),
        label="Статус обслуживания*",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )
    description = forms.CharField(
        label="Описание проверки оборудования",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Дополнительные детали (необязательно)",
        }),
        required=False,
    )
    description_updated = forms.CharField(
        label="Описание обновления",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Опишите изменения (необязательно)",
        }),
        required=False,
    )

    class Meta:
        model = Maintenance
        fields = [
            "equipment",
            "start_time",
            "end_time",
            "status",
            "description",
            "description_updated",
        ]
        labels = {
            "equipment": "Оборудование*",
            "start_time": "Дата и время начала обслуживания*",
            "end_time": "Дата и время конца обслуживания*",
            "status": "Статус обслуживания*",
            "description": "Описание проверки оборудования",
            "description_updated": "Описание обновления",
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Если форма создаётся «для редактирования»
            if self.instance and self.instance.pk:
                # Переводим datetime в строку вида '2025-06-21T14:30'
                self.fields['start_time'].initial = (
                    self.instance.start_time.strftime('%Y-%m-%dT%H:%M')
                )
                self.fields['end_time'].initial = (
                    self.instance.end_time.strftime('%Y-%m-%dT%H:%M')
                )
            # Устанавливаем те же форматы для разбора данных из POST
            self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M']
            self.fields['end_time'].input_formats = ['%Y-%m-%dT%H:%M']