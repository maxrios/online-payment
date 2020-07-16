import stripe
from dotenv import load_dotenv
import os


def add_customer(first_name, last_name, email):
    load_dotenv()
    stripe.api_key = os.getenv("STRIPE_APP_API_KEY")
    name = first_name + ' ' + last_name
    customer = stripe.Customer.create(
        name=name,
        email=email
    )
    return customer.get('id')

# TODO: Implement
def get_customer_info(customer_id):
    load_dotenv()
    stripe.api_key = os.getenv("STRIPE_APP_API_KEY")
    customer = stripe.Customer.retrieve(customer_id)
    return customer

# TODO: Implement
def delete_customer(customer_id):
    load_dotenv()
    stripe.api_key = os.getenv("STRIPE_APP_API_KEY")
    deleted_customer = stripe.Customer.delete(customer_id)
    return deleted_customer


def add_card(customer_id, number, exp_month, exp_year, cvc):
    load_dotenv()
    stripe.api_key = os.getenv("STRIPE_APP_API_KEY")
    try:
        card_token = stripe.Token.create(
            card={
                'number': number,
                'exp_month': exp_month,
                'exp_year': exp_year,
                'cvc': cvc,
            }
        )
        card = stripe.Customer.create_source(
            id=customer_id,
            source=card_token
        )
    except:
        return 'EXPIRED'
    return card.get('id')


def retrieve_card(customer_id, card_id):
    load_dotenv()
    stripe.api_key = os.getenv("STRIPE_APP_API_KEY")
    card_info = stripe.Customer.retrieve_source(
        customer_id,
        card_id
    )
    return card_info


def remove_card(customer_id, card_id):
    load_dotenv()
    stripe.api_key = os.getenv("STRIPE_APP_API_KEY")
    response = stripe.Customer.delete_source(
        customer_id,
        card_id
    )
    return response.get('deleted')

def edit_card(customer_id, card_id, number, exp_month, exp_year, cvc):
    load_dotenv()
    stripe.api_key = os.getenv("STRIPE_APP_API_KEY")
    response = stripe.Customer.modify_source(
        customer_id,
        card_id,
        number=number,
        exp_month=exp_month,
        exp_year=exp_year,
        cvc=cvc
    )
    return response.get('id')