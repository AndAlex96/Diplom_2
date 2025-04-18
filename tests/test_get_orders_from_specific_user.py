import requests
import pytest
import allure
from app.urls import BASE_URL
from app.helpers.auxiliary_functions import get_hash_ingredients_for_order

@allure.title('Тест получения заказов конкретного пользователя')
class TestGetOrderFromUser:

    @allure.step('Проверка получения заказа конкретного пользователя')
    @pytest.mark.parametrize('value, response', [[4, 4], [54, 50]])
    def test_get_order_from_user_with_auth_get_order(self, register_new_user_and_return_email_password_name, value, response):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)

        payload_auth = {"email": email, "password": password}
        response_aurh = requests.post(f'{BASE_URL}api/auth/login', payload_auth)
        response_aurh_token = response_aurh.json().get('accessToken')

        payload_order = get_hash_ingredients_for_order()
        for i in range(value):
             requests.post(f'{BASE_URL}api/orders', data=payload_order, headers={'Authorization':response_aurh_token})
        response_order = requests.get(f'{BASE_URL}api/orders', headers={'Authorization':response_aurh_token})
        response_order_json = response_order.json()
        list_orders = response_order_json['orders']

        assert response_order.status_code == 200
        assert len(list_orders) == response

    @allure.step('Проверка невозможности получения списка заказов конкретного пользователя без авторизации')
    def test_get_order_from_user_without_auth_error_get_order(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)

        payload_auth = {"email": email, "password": password}
        response_aurh = requests.post(f'{BASE_URL}api/auth/login', payload_auth)

        response_aurh_token = response_aurh.json().get('accessToken')
        response_refresh_token = response_aurh.json().get('refreshToken')

        payload_order = get_hash_ingredients_for_order()
        requests.post(f'{BASE_URL}api/orders', data=payload_order, headers={'Authorization': response_aurh_token})

        data_for_out = {"token": response_refresh_token}
        requests.post(f'{BASE_URL}api/auth/logout', data=data_for_out)

        response_order = requests.get(f'{BASE_URL}api/orders')

        assert response_order.status_code == 401
        assert response_order.json() == {"success": False, "message": "You should be authorised"}
