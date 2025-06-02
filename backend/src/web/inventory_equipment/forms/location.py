from django import forms
from apps.locations.models import Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'description']
        labels = {
            'name': 'Название местоположения',
            'description': 'Описание местоположения',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название местоположения'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание',
                'rows': 3
            }),
        }