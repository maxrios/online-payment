from django.shortcuts import render, redirect
from stripe_access.src import card_access
from .models import Cards
from django.contrib.auth.decorators import login_required
from card.forms import NewCardForm, RemoveCardForm


@login_required(login_url='/user/login/')
def add_card(request):
    if request.method == 'POST':
        form = NewCardForm(request.POST)
        if form.is_valid():
            card = card_access.add_card(
                request.user.profile.customer_id,
                form.cleaned_data.get('number'),
                int(form.cleaned_data.get('exp_month')),
                int(form.cleaned_data.get('exp_year')),
                form.cleaned_data.get('cvc')
            )
            card = Cards(profile=request.user.profile, card_id=card)
            card.save()
            return redirect('home')
    else:
        form = NewCardForm()
    return render(request, 'card_registration.html', {'form': form})


@login_required(login_url='/user/login/')
def remove_card(request):
    if request.method == 'POST':
        form = RemoveCardForm(request.user, request.POST)
        if form.is_valid():
            if card_access.remove_card(request.user.profile.customer_id, form.cleaned_data.get('card')):
                Cards.objects.filter(card_id=form.cleaned_data.get('card')).delete()
            return redirect('removecard')
    else:
        form = RemoveCardForm(request.user)
    return render(request, 'card_list.html', {'form': form})
