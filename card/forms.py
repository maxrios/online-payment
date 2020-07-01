from django import forms
from stripe_access.src.card_access import retrieve_card

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


class RemoveCardForm(forms.Form):
    card = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, user, *args, **kwargs):
        super(RemoveCardForm, self).__init__(*args, **kwargs)

        cards = user.profile.cards_info.all()
        print(cards)
        choices = []
        for card in cards:
            card_info = retrieve_card(user.profile.customer_id, card.card_id)
            display = card_info.get('last4') + ' - ' + str(card_info.get('exp_month')) + '/' + str(card_info.get('exp_year'))
            choices.append((card.card_id, display))

        self.fields['card'].choices = choices
