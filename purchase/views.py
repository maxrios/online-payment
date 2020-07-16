from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CreatePurchaseForm
from stripe_access.src import purchase_access
from purchase.models import Purchase
from card.models import Cards



@login_required(login_url='/user/login/')
def create_purchase(request):
    if request.method == 'POST':
        form = CreatePurchaseForm(request.user, request.POST)
        if form.is_valid():
            print("PAY SUCCESS!!!")
            # TODO: Implement payment intent error handling
            payment_id = purchase_access.create_purchase(
                amount=form.cleaned_data.get('amount'),
                receipt_email=request.user.email,
                payment_method=form.cleaned_data.get('payment_method'),
                customer_id=request.user.profile.customer_id
            )
            print('Payment ID: ' + payment_id)
            payment = Purchase(purchase_id=payment_id, customer_id=request.user.profile.customer_id)
            payment.save()
            return redirect('home')
    else:
        if not Cards.objects.filter(profile=request.user.profile) :
            return redirect('addcard')
        form = CreatePurchaseForm(request.user)
    return render(request, 'purchase/create_purchase.html', {'form': form})


@staff_member_required
def view_all_purchases(request):
    context = {
        'purchases': Purchase.objects.all(),
    }
    return render(request, 'purchase/all_purchases.html', context)