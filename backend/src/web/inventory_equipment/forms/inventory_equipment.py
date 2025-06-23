from django import forms
from apps.equipments.models.inventory_equipment import InventoryEquipment
from apps.equipments.models.inventory_equipment_status import InventoryEquipmentStatus
from apps.locations.models import Location


class InventoryEquipmentForm(forms.ModelForm):
    name = forms.CharField(
        label="Название*",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите название оборудования"
        }),
        required=True,
        max_length=100,
    )
    inventory_number = forms.CharField(
        label="Штрихкод",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите штрихкод"
        }),
        required=False,
        max_length=32,
    )
    count = forms.IntegerField(
        label="Количество*",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Введите количество"
        }),
        required=True,
        min_value=1,
    )
    photo = forms.ImageField(
        label="Фото",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        required=False,
    )
    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Введите описание",
            "rows": 3,
        }),
        required=False,
    )
    status = forms.ModelChoiceField(
        queryset=InventoryEquipmentStatus.objects.all(),
        label="Статус",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        label="Локация*",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )

    class Meta:
        model = InventoryEquipment
        # owner убран: задаём его только на сервере
        fields = [
            "name",
            "inventory_number",
            "photo",
            "description",
            "status",
            "location",
            "count",
        ]
