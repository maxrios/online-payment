from user.forms import SignUpForm, NewCardForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from stripe_access.src import card_access
from user.models import Cards
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user    = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.customer_id = card_access.add_customer(
                form.cleaned_data.get('first_name'),
                form.cleaned_data.get('last_name'),
                form.cleaned_data.get('email')
            )
            user.save()
            raw_password    = form.cleaned_data.get('password1')
            user            = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

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
