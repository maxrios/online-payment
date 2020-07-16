from django.shortcuts import render, redirect
from stripe_access.src import card_access
from .models import Cards
from django.contrib.auth.decorators import login_required
from card.forms import NewCardForm, EditCardForm, RemoveCardForm


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
            # TODO: Add proper error handling for expired cards
            if card == 'EXPIRED':
                return redirect('home')
            card = Cards(profile=request.user.profile, card_id=card)
            card.save()
            return redirect('home')
    else:
        form = NewCardForm()
    return render(request, 'card/card_registration.html', {'form': form})


@login_required(login_url='/user/login/')
def edit_card(request):
    if request.method == 'POST':
        form = EditCardForm(request.POST)
        if form.is_valid():
            print('CARD: ' + request.POST.get('card'))
            Cards.objects.filter(card_id=request.POST.get('card')).card_id = card_access.edit_card(
                request.user.profile.customer_id,
                request.POST.get('card'), 
                form.cleaned_data.get('number'),
                int(form.cleaned_data.get('exp_month')),
                int(form.cleaned_data.get('exp_year')),
                form.cleaned_data.get('cvc'),
            )
            print("NEW CARD: " + Cards.objects.filter(card_id=request.POST.get('card')).card_id)
            return redirect('removecard')
        else:
            print("FAILED!!!")
            print(form.errors)
    else:
        selected_card = request.session.pop('selected_card', {})
        form = EditCardForm({'number': selected_card.get('number'),
            'exp_month': int(selected_card.get('exp_month')),
            'exp_year': int(selected_card.get('exp_year')),
            'exp_month': selected_card.get('cvc'),
          })
    return render(request, 'card/card_edit.html', {'form': form})


# TODO: Add edit card function
@login_required(login_url='/user/login/')
def remove_card(request):
    if request.method == 'POST':
            form = RemoveCardForm(request.user, request.POST)
            if form.is_valid():
                if 'edit-card' in request.POST:
                    card = card_access.retrieve_card(request.user.profile.customer_id, form.cleaned_data.get('card'))
                    form_edit = EditCardForm({
                        'number': card.get('number'),
                        'exp_month': card.get('exp_month'),
                        'exp_year': card.get('exp_year'),
                        'exp_month': card.get('cvc'),
                    })
                    print('POP')
                else:
                    if card_access.remove_card(request.user.profile.customer_id, form.cleaned_data.get('card')):
                        Cards.objects.filter(card_id=form.cleaned_data.get('card')).delete()
                    return redirect('removecard')
    else:
        if not Cards.objects.filter(profile=request.user.profile) :
            return redirect('addcard')
        form = RemoveCardForm(request.user)
        form_edit   = EditCardForm()
    return render(request, 'card/card_list.html', {'form': form, 'form_edit': form_edit})
