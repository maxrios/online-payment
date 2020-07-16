from django import forms
from stripe_access.src.card_access import retrieve_card

class NewCardForm(forms.Form):
    number      = forms.CharField(max_length=16, required=True)
    exp_month   = forms.IntegerField(required=True)
    exp_year    = forms.IntegerField(required=True)
    cvc         = forms.CharField(max_length=3, required=True)

    def __init__(self, *args, **kwargs):
        super(NewCardForm, self).__init__(*args, **kwargs)
        self.fields['exp_month'].widget.attrs['placeholder'] = 'MM'
        self.fields['exp_year'].widget.attrs['placeholder'] = 'YYYY'

    def clean_number(self):
        number = ''.join((self.cleaned_data['number']).split())
        if len(number) != 16:
            raise forms.ValidationError('Enter a correct card number.')
        return number

    def clean_exp_month(self):
        exp_m = self.cleaned_data['exp_month']
        if exp_m > 12 or exp_m < 1:
            raise forms.ValidationError('Enter a correct experation month.')
        return exp_m

    def clean_cvc(self):
        cvc = self.cleaned_data['cvc']
        if len(cvc) != 3:
            raise forms.ValidationError('Enter a correct cvc number.')


class EditCardForm(forms.Form):
    number      = forms.CharField(max_length=16, required=True)
    exp_month   = forms.IntegerField(required=True)
    exp_year    = forms.IntegerField(required=True)
    cvc         = forms.CharField(max_length=3, required=True)

    def __init__(self, *args, **kwargs):
        super(EditCardForm, self).__init__(*args, **kwargs)
        self.fields['exp_month'].widget.attrs['placeholder'] = 'MM'
        self.fields['exp_year'].widget.attrs['placeholder'] = 'YYYY'

    def clean_number(self):
        number = ''.join((self.cleaned_data['number']).split())
        if len(number) != 16 and len(number) != 0:
            raise forms.ValidationError('Enter a correct card number.')
        return number

    def clean_exp_month(self):
        exp_month = self.cleaned_data['exp_month']
        if exp_month is not None:
            if (exp_month > 12 or exp_month < 1):
                raise forms.ValidationError('Enter a correct experation month.')
        return exp_month

    def clean_cvc(self):
        cvc = self.cleaned_data['cvc']
        if len(cvc) != 3 and len(cvc) != 0:
            raise forms.ValidationError('Enter a correct cvc number.')



class RemoveCardForm(forms.Form):
    card = forms.ChoiceField(widget=forms.RadioSelect, required=True, label='')

    def __init__(self, user, *args, **kwargs):
        super(RemoveCardForm, self).__init__(*args, **kwargs)
        self.fields['card'].widget.attrs['class'] = 'list-unstyled'
        cards = user.profile.cards_info.all()
        choices = []
        for card in cards:
            card_info = retrieve_card(user.profile.customer_id, card.card_id)
            display = card_info.get('last4') + ' - ' + str(card_info.get('exp_month')) + '/' + str(card_info.get('exp_year'))
            choices.append((card.card_id, display))

        self.fields['card'].choices = choices
        if choices:
            self.fields['card'].initial = choices[0][0]
        
