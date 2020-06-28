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
