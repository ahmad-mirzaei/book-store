from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            "full_name",
            "phone",
            "address",
            "postal_code",
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام و نام خانوادگی",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "شماره تماس",
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "آدرس کامل",
            }),
            "postal_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "کد پستی (اختیاری)",
            }),
        }