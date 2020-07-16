import stripe
from dotenv import load_dotenv
import os


def create_purchase(amount, receipt_email, payment_method, customer_id):
    load_dotenv()
    stripe.api_key = os.getenv("STRIPE_APP_API_KEY")
    payment = stripe.PaymentIntent.create(
        amount=amount,
        confirm=True,
        currency='usd',
        receipt_email=receipt_email,
        payment_method=payment_method,
        customer=customer_id
    )
    print('STATUS: ' + payment.get('status'))
    return payment.get('id')
    