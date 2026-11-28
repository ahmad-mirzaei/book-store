from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    
    def clean_address(self):
        address = self.cleaned_data["address"].strip()

        if len(address) < 10:
            raise forms.ValidationError(
                "آدرس باید حداقل ۱۰ کاراکتر باشد."
            )

        return address
    
    def clean_postal_code(self):
        postal_code = self.cleaned_data.get("postal_code", "").strip()

        if postal_code and (
            not postal_code.isdigit() or len(postal_code) != 10
        ):
            raise forms.ValidationError(
                "کد پستی باید دقیقاً ۱۰ رقم باشد."
            )

        return postal_code
    
    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        if not phone.isdigit():
            raise forms.ValidationError("شماره تماس باید فقط شامل اعداد باشد.")

        if len(phone) != 11 or not phone.startswith("09"):
            raise forms.ValidationError("شماره تماس باید ۱۱ رقم و با 09 شروع شود.")

        return phone
    
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
                "placeholder": "لطفاً آدرس را کامل و دقیق وارد کنید",
            }),
            "postal_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "کد پستی ۱۰ رقمی",
            }),
        }