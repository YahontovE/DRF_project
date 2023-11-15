import requests

from config.settings import SECRET_KEY_STRIPE


def create_payment_intent(amount, currency='USD'):
    headers = {'Authorization': f'Bearer {SECRET_KEY_STRIPE}'}
    params = {'amount': amount, 'currency': currency}
    response = requests.post('https://api.stripe.com/v1/payment_intents', headers=headers, params=params)
    data = response.json()
    return data['id']


def retrieve_payment_intent(payment_id):
    headers = {'Authorization': f'Bearer {SECRET_KEY_STRIPE}'}
    response = requests.get(f'https://api.stripe.com/v1/payment_intents/{payment_id}', headers=headers)

    return response.json()