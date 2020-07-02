from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class SignUpForm(UserCreationForm):
    first_name  = forms.CharField(max_length=30, required=True)
    last_name   = forms.CharField(max_length=30, required=True)
    email       = forms.EmailField(max_length=254)
    birth_date  = forms.DateField(help_text=mark_safe('<br>Format: MM/DD/YYYY.'))

    class Meta:
        model   = User
        fields  = ('first_name', 'last_name', 'birth_date', 'email', 'username', 'password1', 'password2')
