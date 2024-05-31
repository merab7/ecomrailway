from django import forms
from .models import ShippingAddress
from django.core.validators import RegexValidator
from datetime import datetime
from django.utils.translation import gettext_lazy as _

class ShippingInfo(forms.ModelForm):
    fullname = forms.CharField(label=_("Fullname"), widget=forms.TextInput(attrs={'class':'form_control', 'placeholder':'Full Name' }), required=True)
    email = forms.CharField(label=_("Email"), widget=forms.TextInput(attrs={'class':'form_control', 'placeholder': 'Email' }), required=True)
    address = forms.CharField(label=_("Address"), widget=forms.TextInput(attrs={'class':'form_control', 'placeholder': 'Address' }), required=True)
    city = forms.CharField(label=_("City"), widget=forms.TextInput(attrs={'class':'form_control', 'placeholder': 'City' }), required=True)
    zipcode = forms.CharField(label=_("Zip"), widget=forms.TextInput(attrs={'class':'form_control', 'placeholder': 'Zipcode' }), required=False)
    phone = forms.CharField(label=_("Phone"), widget=forms.TextInput(attrs={'class':'form_control', 'placeholder': 'Phone' }), required=True)
    add_information = forms.CharField(label=_("Extra-Info"), widget=forms.Textarea(attrs={'class':'form_control', 'placeholder': 'Additional Information' }), required=False)
    per_id = forms.CharField(label=_("ID NUM"), widget=forms.TextInput(attrs={'class':'form_control', 'placeholder': 'Personal Id' }), required=True)
    class Meta:
        model = ShippingAddress
        fields = ["fullname", "email", "address", "city","phone", "zipcode", "per_id", "add_information"]




class PaymentForm(forms.Form):
    card_number = forms.CharField(
        label=_("Card Number"),
        widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': '1234-5678-9012-3456'}),
        required=True,
        validators=[
            RegexValidator(
                regex=r'^(\d{4}-){3}\d{4}$',
                message=_('Card number must be in the format XXXX-XXXX-XXXX-XXXX.')
            )
        ]
    )
    name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Name'}),
        required=True
    )
    expiration = forms.CharField(
        label=_("Expiration Date"),
        widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'MM/YY'}),
        required=True,
        validators=[
            RegexValidator(
                regex=r'^(0[1-9]|1[0-2])\/\d{2}$',
                message='Expiration date must be in the format MM/YY.'
            )
        ]
    )
    cvv = forms.CharField(
        label="CVV",
        widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'CVV', 'type': 'password'}),
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3,4}$',
                message='CVV must be 3 or 4 digits.'
            )
        ]
    )

    def clean_expiration(self):
        expiration = self.cleaned_data.get('expiration')
        if expiration:
            current_year = datetime.now().year % 100  # Get last two digits of current year
            current_month = datetime.now().month

            exp_month, exp_year = map(int, expiration.split('/'))
            if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
                raise forms.ValidationError("The expiration date cannot be in the past.")
        return expiration