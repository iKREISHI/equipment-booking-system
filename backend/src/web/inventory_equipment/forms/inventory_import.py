from django import forms
from apps.equipments.models import InventoryImport


class InventoryImportForm(forms.ModelForm):
    class Meta:
        model = InventoryImport
        fields = ("file",)
        widgets = {
            "file": forms.ClearableFileInput(
                attrs={
                    "accept": ".xlsx",
                    "class": "form-control",
                }
            ),
        }
        labels = {"file": "Файл Excel (.xlsx)"}
