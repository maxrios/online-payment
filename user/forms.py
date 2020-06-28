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


class NewCardForm(forms.Form):
    number      = forms.CharField(max_length=16, required=True, help_text='Required.')
    exp_month   = forms.IntegerField(required=True, help_text='Required.')
    exp_year    = forms.IntegerField(required=True, help_text='Required.')
    cvc         = forms.CharField(max_length=3, required=True, help_text='Required.')

    def clean_number(self):
        number = ''.join((self.cleaned_data['number']).split())
        if len(number) != 16:
            raise forms.ValidationError('Enter a correct card number.')
        return number

    def clean_exp_month(self):
        exp_month = self.cleaned_data['exp_month']
        if exp_month > 12 or exp_month < 1:
            raise forms.ValidationError('Enter a correct experation month.')
        return exp_month

    def clean_cvc(self):
        cvc = self.cleaned_data['cvc']
        if len(cvc) != 3:
            raise forms.ValidationError('Enter a correct cvc number.')
