from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

class SignUpForm(UserCreationForm):
    username = forms.CharField(label=_('username'), max_length=30)
    email = forms.EmailField(label=_('email'), max_length=200)
    first_name = forms.CharField(label=_('first name'), max_length=100 )
    last_name = forms.CharField(label=_('last name'), max_length=100)
    address = forms.CharField(label=_('address'), max_length=200)
    city = forms.CharField(label=_('city'), max_length=200)
    phone = forms.CharField(label=_('Phone'), max_length=200)
    zipcode = forms.CharField(label=_('zipcode'), max_length=200)



    class Meta:
        model = User
        fields = ( 'username', 'first_name', 'last_name',
'email', 'password1', 'password2', 'city', 'address', 'phone', 'zipcode'  )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email = email).exists():
            raise ValidationError("An user with this email already exists!")
        return email

        
        

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name','city', 'address', 'phone', 'zipcode', ]

