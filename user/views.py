from user.forms import SignUpForm, NewCardForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from stripe_access.src.card_access import add_customer


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user    = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.customer_id = add_customer(
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


def add_card(request):
    if request.method == 'POST':
        form = NewCardForm(request.POST)
        if form.is_valid():
            pass
            return redirect('home')
    else:
        form = NewCardForm()
    return render(request, 'card_registration.html', {'form': form})
