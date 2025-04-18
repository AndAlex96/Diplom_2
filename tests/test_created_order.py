import requests
import allure
from app.urls import BASE_URL
from app.helpers.auxiliary_functions import get_hash_ingredients_for_order

@allure.title('Тест создания заказа')
class TestCreatedOrder:

    @allure.step('Проверка создания заказа с ингридиентами авторизованным пользователем')
    def test_created_order_with_auth_and_with_ingredients_success_order(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)

        payload_auth = {"email": email, "password": password}
        requests.post(f'{BASE_URL}api/auth/login', payload_auth)

        payload_order = get_hash_ingredients_for_order()
        response_order = requests.post(f'{BASE_URL}api/orders', data=payload_order)

        assert response_order.status_code == 200
        assert 'name', 'order' in response_order.json()
        assert response_order.json().get('success') == True

    @allure.step('Проверка создания заказа с ингридиентами неавторизованным пользователем')
    def test_created_order_without_auth_and_with_ingredients_error_order(self):

        payload_order = get_hash_ingredients_for_order()
        response_order = requests.post(f'{BASE_URL}api/orders', json=payload_order)

        assert response_order.status_code == 401, f"Ожидался статус 401, но получен {response_order.status_code}"
        #тело отсутствует в требованиях, в уточнении по серой зоне дали ответ только по коду

    @allure.step('Проверка создания заказа без ингридиентов авторизованным пользователем')
    def test_created_order_with_auth_and_without_ingredients_error_order(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)

        payload_auth = {"email": email, "password": password}
        requests.post(f'{BASE_URL}api/auth/login', payload_auth)

        payload_order = {"ingredients": []}
        response_order = requests.post(f'{BASE_URL}api/orders', data=payload_order)

        assert response_order.status_code == 400
        assert response_order.json() == {
            "success": False,
            "message": "Ingredient ids must be provided"
        }

    @allure.step('Проверка создания заказа без ингридиентов неавторизованным пользователем')
    def test_created_order_without_auth_and_without_ingredients_error_order(self):
        payload_order = {"ingredients": []}
        response_order = requests.post(f'{BASE_URL}api/orders', data=payload_order)

        assert response_order.status_code == 400

    @allure.step('Проверка создания заказа с неверным хэшем ингридиентов авторизованным пользователем')
    def test_created_order_with_auth_and_with_incorrect_hash_ingredients_error_order(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)

        payload_auth = {"email": email, "password": password}
        requests.post(f'{BASE_URL}api/auth/login', payload_auth)

        get_hash_ingredients = requests.get(f'{BASE_URL}api/ingredients')
        get_hash_ingredients_json = get_hash_ingredients.json()

        ingredients = get_hash_ingredients_json['data']
        ingredients1 = ingredients[0]['_id']
        ingredients2 = ingredients[1]['_id']
        payload_order = {"ingredients": [f'1{ingredients1}', f'1{ingredients2}']}

        response_order = requests.post(f'{BASE_URL}api/orders', data=payload_order)

        assert response_order.status_code == 500
        #при уточнении по серой зоне дели ответ, что никакое тело не должно вернуться

    @allure.step('Проверка создания заказа с неверным хэшем ингридиентов неавторизованным пользователем')
    def test_created_order_without_auth_and_with_incorrect_hash_ingredients_error_order(self, register_new_user_and_return_email_password_name):
        get_hash_ingredients = requests.get(f'{BASE_URL}api/ingredients')
        get_hash_ingredients_json = get_hash_ingredients.json()

        ingredients = get_hash_ingredients_json['data']
        ingredients1 = ingredients[0]['_id']
        ingredients2 = ingredients[1]['_id']
        payload_order = {"ingredients": [f'1{ingredients1}', f'1{ingredients2}']}
        response_order = requests.post(f'{BASE_URL}api/orders', data=payload_order)

        assert response_order.status_code == 500
        #статус 500 из расчета не на неавторизованного пользователя, а на передачу несуществующих хэшей ингридиентов
