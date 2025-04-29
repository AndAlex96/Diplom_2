import requests
import pytest
import allure
from app.urls import URL_AUTH_LOGOUT, URL_AUTH_LOGIN, URL_AUTH_REGISTER, URL_ORDERS
from app.helpers.auxiliary_functions import get_hash_ingredients_for_order

@allure.title('Тест получения заказов конкретного пользователя')
class TestGetOrderFromUser :

    @allure.step('Проверка получения заказа конкретного пользователя')
    @pytest.mark.parametrize('value, response', [[4, 4], [54, 50]])
    def test_get_order_from_user_with_auth_get_order(self, register_new_user_and_return_email_password_name, value, response):
        with allure.step('Регистрация нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"email": email, "password": password, "name": name}
            requests.post(url=URL_AUTH_REGISTER, data=payload)

        with allure.step('Авторизация пользователя'):
            payload_auth = {"email": email, "password": password}
            response_auth = requests.post(URL_AUTH_LOGIN, payload_auth)
            response_auth_token = response_auth.json().get('accessToken')

        with allure.step('Создание заказов'):
            payload_order = get_hash_ingredients_for_order()
            for i in range(value):
                requests.post(url=URL_ORDERS, data=payload_order, headers={'Authorization': response_auth_token})

        with allure.step('Получение списка заказов'):
            response_order = requests.get(url=URL_ORDERS, headers={'Authorization': response_auth_token})
            response_order_json = response_order.json()
            list_orders = response_order_json['orders']

        assert response_order.status_code == 200
        assert len(list_orders) == response

    @allure.step('Проверка невозможности получения списка заказов конкретного пользователя без авторизации')
    def test_get_order_from_user_without_auth_error_get_order(self, register_new_user_and_return_email_password_name):
        with allure.step('Регистрация нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"email": email, "password": password, "name": name}
            requests.post(url=URL_AUTH_REGISTER, data=payload)

        with allure.step('Авторизация пользователя'):
            payload_auth = {"email": email, "password": password}
            response_auth = requests.post(URL_AUTH_LOGIN, payload_auth)
            response_auth_token = response_auth.json().get('accessToken')
            response_refresh_token = response_auth.json().get('refreshToken')

        with allure.step('Создание заказа'):
            payload_order = get_hash_ingredients_for_order()
            requests.post(url=URL_ORDERS, data=payload_order, headers={'Authorization': response_auth_token})

        with allure.step('Выход из системы'):
            data_for_out = {"token": response_refresh_token}
            requests.post(url=URL_AUTH_LOGOUT, data=data_for_out)

        with allure.step('Попытка получения списка заказов без авторизации'):
            response_order = requests.get(url=URL_ORDERS)

        assert response_order.status_code == 401
        assert response_order.json() == {"success": False, "message": "You should be authorised"}
