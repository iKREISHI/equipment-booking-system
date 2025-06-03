from django import forms
from apps.equipments.models.inventory_equipment import InventoryEquipment
from apps.users.models.users import User
from apps.equipments.models.inventory_equipment_status import InventoryEquipmentStatus
from apps.locations.models import Location

class InventoryEquipmentForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True).all(),
        label="Владелец*",
        widget=forms.Select(attrs={
            "class": "form-select",
            "placeholder": "Выберите владельца"
        }),
        required=True
    )
    name = forms.CharField(
        label="Название*",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите название оборудования"
        }),
        required=True,
        max_length=100
    )
    inventory_number = forms.CharField(
        label="Штрихкод*",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Введите штрихкод"
        }),
        required=True,
        max_length=32
    )
    photo = forms.ImageField(
        label="Фото",
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control"
        }),
        required=False
    )
    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Введите описание",
            "rows": 3
        }),
        required=False
    )
    status = forms.ModelChoiceField(
        queryset=InventoryEquipmentStatus.objects.all(),
        label="Статус",
        widget=forms.Select(attrs={
            "class": "form-select"
        }),
        required=False
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        label="Локация*",
        widget=forms.Select(attrs={
            "class": "form-select"
        }),
        required=True
    )

    class Meta:
        model = InventoryEquipment
        fields = [
            "owner",
            "name",
            "inventory_number",
            "photo",
            "description",
            "status",
            "location",
        ]
