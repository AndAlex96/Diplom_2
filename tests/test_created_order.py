import requests
import allure
from app.urls import URL_AUTH_REGISTER, URL_AUTH_LOGIN, URL_ORDERS, URL_INGREDIENTS
from app.helpers.auxiliary_functions import get_hash_ingredients_for_order

@allure.title('Тест создания заказа')
class TestCreatedOrder:

    @allure.step('Проверка создания заказа с ингредиентами авторизованным пользователем')
    def test_created_order_with_auth_and_with_ingredients_success_order(self, register_new_user_and_return_email_password_name):
        with allure.step('Регистрация нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"email": email, "password": password, "name": name}
            requests.post(url=URL_AUTH_REGISTER, data=payload)

        with allure.step('Авторизация пользователя'):
            payload_auth = {"email": email, "password": password}
            requests.post(URL_AUTH_LOGIN, payload_auth)

        with allure.step('Создание заказа с ингредиентами'):
            payload_order = get_hash_ingredients_for_order()
            response_order = requests.post(url=URL_ORDERS, data=payload_order)

        assert response_order.status_code == 200
        assert 'name' in response_order.json() and 'order' in response_order.json()
        assert response_order.json().get('success') is True

    @allure.step('Проверка создания заказа с ингредиентами неавторизованным пользователем')
    def test_created_order_without_auth_and_with_ingredients_error_order(self):
        with allure.step('Попытка создания заказа без авторизации'):
            payload_order = get_hash_ingredients_for_order()
            response_order = requests.post(url=URL_ORDERS, json=payload_order)

        assert response_order.status_code == 401, f"Ожидался статус 401, но получен {response_order.status_code}"

    @allure.step('Проверка создания заказа без ингредиентов авторизованным пользователем')
    def test_created_order_with_auth_and_without_ingredients_error_order(self, register_new_user_and_return_email_password_name):
        with allure.step('Регистрация нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"email": email, "password": password, "name": name}
            requests.post(url=URL_AUTH_REGISTER, data=payload)

        with allure.step('Авторизация пользователя'):
            payload_auth = {"email": email, "password": password}
            requests.post(URL_AUTH_LOGIN, payload_auth)

        with allure.step('Попытка создания заказа без ингредиентов'):
            payload_order = {"ingredients": []}
            response_order = requests.post(url=URL_ORDERS, data=payload_order)

        assert response_order.status_code == 400
        assert response_order.json() == {
            "success": False,
            "message": "Ingredient ids must be provided"
        }

    @allure.step('Проверка создания заказа без ингредиентов неавторизованным пользователем')
    def test_created_order_without_auth_and_without_ingredients_error_order(self):
        with allure.step('Попытка создания заказа без авторизации и без ингредиентов'):
            payload_order = {"ingredients": []}
            response_order = requests.post(url=URL_ORDERS, data=payload_order)

        assert response_order.status_code == 400

    @allure.step('Проверка создания заказа с неверным хэшем ингредиентов авторизованным пользователем')
    def test_created_order_with_auth_and_with_incorrect_hash_ingredients_error_order(self,
                                                                                     register_new_user_and_return_email_password_name):
        with allure.step('Регистрация нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"email": email, "password": password, "name": name}
            requests.post(url=URL_AUTH_REGISTER, data=payload)

        with allure.step('Авторизация пользователя'):
            payload_auth = {"email": email, "password": password}
            requests.post(URL_AUTH_LOGIN, payload_auth)

        with allure.step('Получение хэшей ингредиентов'):
            get_hash_ingredients = requests.get(URL_INGREDIENTS)
            get_hash_ingredients_json = get_hash_ingredients.json()

        with allure.step('Формирование неверных хэшей ингредиентов'):
            ingredients = get_hash_ingredients_json['data']
            ingredients1 = ingredients[0]['_id']
            ingredients2 = ingredients[1]['_id']
            payload_order = {"ingredients": [f'1{ingredients1}', f'1{ingredients2}']}

        with allure.step('Попытка создания заказа с неверными хэшами ингредиентов'):
            response_order = requests.post(url=URL_ORDERS, data=payload_order)

        assert response_order.status_code == 500
        # При уточнении по серой зоне дали ответ, что никакое тело не должно вернуться

    @allure.step('Проверка создания заказа с неверным хэшем ингредиентов неавторизованным пользователем')
    def test_created_order_without_auth_and_with_incorrect_hash_ingredients_error_order(self,
                                                                                        register_new_user_and_return_email_password_name):
        with allure.step('Получение хэшей ингредиентов'):
            get_hash_ingredients = requests.get(URL_INGREDIENTS)
            get_hash_ingredients_json = get_hash_ingredients.json()

        with allure.step('Формирование неверных хэшей ингредиентов'):
            ingredients = get_hash_ingredients_json['data']
            ingredients1 = ingredients[0]['_id']
            ingredients2 = ingredients[1]['_id']
            payload_order = {"ingredients": [f'1{ingredients1}', f'1{ingredients2}']}

        with allure.step('Попытка создания заказа с неверными хэшами ингредиентов'):
            response_order = requests.post(url=URL_ORDERS, data=payload_order)

        assert response_order.status_code == 500
        # Статус 500 из расчета не на неавторизованного пользователя, а на передачу несуществующих хэшей ингредиентов
