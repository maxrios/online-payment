from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name  = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name   = forms.CharField(max_length=30, required=True, help_text='Required.')
    email       = forms.EmailField(max_length=254, help_text='Required. Include a valid email address.')
    birth_date  = forms.DateField(help_text='Required. Format: MM/DD/YYYY.')
    # customer_id = forms.CharField(max_length=100)

    class Meta:
        model   = User
        fields  = ('first_name', 'last_name', 'birth_date', 'email', 'username', 'password1', 'password2')
