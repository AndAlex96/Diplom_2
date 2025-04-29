import requests
import allure
from app.urls import URL_AUTH_REGISTER, URL_AUTH_LOGIN

@allure.title('Тест входа в аккаунт пользователя')
class TestLogin:

    @allure.step('Проверка входа в аккаунт с корректными данными')
    def test_login_with_correct_data_success_login(self, register_new_user_and_return_email_password_name):
        with allure.step('Получение данных нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"email": email, "password": password, "name": name}
            requests.post(url=URL_AUTH_REGISTER, data=payload)

        with allure.step('Авторизация пользователя'):
            payload_auth = {"email": email, "password": password}
            response_auth = requests.post(URL_AUTH_LOGIN, payload_auth)
            response_auth_json = response_auth.json()
            token_auth = response_auth_json.get('accessToken')
            token_out = response_auth_json.get('refreshToken')

        assert response_auth.status_code == 200
        assert response_auth.json() == {
            "success": True,
            "accessToken": token_auth,
            "refreshToken": token_out,
            "user": {
                "email": email,
                "name": name
            }
        }

    @allure.step('Проверка невозможности входа в аккаунт с некорректным email')
    def test_login_with_incorrect_email_error_login(self, register_new_user_and_return_email_password_name):
        with allure.step('Регистрация нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"email": email, "password": password, "name": name}
            requests.post(url=URL_AUTH_REGISTER, data=payload)

        with allure.step('Попытка авторизации с некорректным email'):
            payload_auth = {"email": f'1{email}', "password": password}
            response_auth = requests.post(URL_AUTH_LOGIN, payload_auth)

        assert response_auth.status_code == 401
        assert response_auth.json() == {
            "success": False,
            "message": "email or password are incorrect"
        }

    @allure.step('Проверка невозможности входа в аккаунт с некорректным паролем')
    def test_login_with_incorrect_password_error_login(self, register_new_user_and_return_email_password_name):
        with allure.step('Регистрация нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"email": email, "password": password, "name": name}
            requests.post(url=URL_AUTH_REGISTER, data=payload)

        with allure.step('Попытка авторизации с некорректным паролем'):
            payload_auth = {"email": email, "password": f'1{password}'}
            response_auth = requests.post(URL_AUTH_LOGIN, payload_auth)

        assert response_auth.status_code == 401
        assert response_auth.json() == {
            "success": False,
            "message": "email or password are incorrect"
        }