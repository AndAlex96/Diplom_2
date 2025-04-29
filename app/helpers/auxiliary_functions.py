import random
import string
import requests
from app.urls import URL_INGREDIENTS

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_email_password_name():
    email = f'{generate_random_string(6)}@yandex.ru'
    password = generate_random_string(8)
    name = generate_random_string(8)
    return [email, password, name]

def get_hash_ingredients_for_order():
    get_hash_ingredients = requests.get(URL_INGREDIENTS)
    get_hash_ingredients_json = get_hash_ingredients.json()

    ingredients = get_hash_ingredients_json['data']
    ingredients1 = ingredients[0]['_id']
    ingredients2 = ingredients[1]['_id']
    payload_order = {"ingredients": [ingredients1, ingredients2]}

    return payload_order