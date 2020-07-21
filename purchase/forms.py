from django import forms
from stripe_access.src.card_access import retrieve_card


class CreatePurchaseForm(forms.Form):
    amount          =   forms.IntegerField(required=True)
    payment_method  =   forms.ChoiceField(widget=forms.RadioSelect, required=True, label='')

    def __init__(self, user, *args, **kwargs):
        super(CreatePurchaseForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'].widget.attrs['class'] = 'list-unstyled'
        self.fields['amount'].widget.attrs['placeholder'] = 'Enter in lowest currency'
        cards = user.profile.cards_info.all()
        choices = []
        for card in cards:
            card_info = retrieve_card(user.profile.customer_id, card.card_id)
            display = card_info.get('last4') + ' - ' + str(card_info.get('exp_month')) + '/' + str(card_info.get('exp_year'))
            choices.append((card.card_id, display))

        self.fields['payment_method'].choices = choices
        if choices:
            self.fields['payment_method'].initial = choices[0][0]
