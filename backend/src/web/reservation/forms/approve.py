from django import forms

class RejectReasonForm(forms.Form):
    status_response = forms.CharField(
        label="Причина отказа*",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Укажите причину отклонения заявки"
        }),
        required=True,
    )