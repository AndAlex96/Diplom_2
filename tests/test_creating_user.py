import requests
import allure
from app.urls import URL_AUTH_REGISTER

@allure.title('Тест создания пользователя')
class TestCreatingUser :

    @allure.step('Проверка создания пользователя с корректными данными')
    def test_creating_new_user_with_correct_data_successful_registration(self, register_new_user_and_return_email_password_name):
        with allure.step('Получение данных нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"email": email, "password": password, "name": name}

        with allure.step('Регистрация нового пользователя'):
            response = requests.post(url=URL_AUTH_REGISTER, data=payload)
            response_body = response.json()
            get_token_access = response_body.get('accessToken')
            get_token_refresh = response_body.get('refreshToken')

        assert response.status_code == 200
        assert response_body == {
            "success": True,
            "user": {
                "email": email,
                "name": name
            },
            "accessToken": get_token_access,
            "refreshToken": get_token_refresh
        }

    @allure.step('Проверка невозможности повторного создания аккаунта с аналогичными данными')
    def test_creating_user_which_is_already_registered_error_registration(self, register_new_user_and_return_email_password_name):
        with allure.step('Получение данных нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"email": email, "password": password, "name": name}

        with allure.step('Регистрация нового пользователя'):
            requests.post(url=URL_AUTH_REGISTER, data=payload)

        with allure.step('Попытка повторной регистрации'):
            response = requests.post(url=URL_AUTH_REGISTER, data=payload)
            response_body = response.json()

        assert response.status_code == 403
        assert response_body == {
            "success": False,
            "message": "User already exists"
        }

    @allure.step('Проверка невозможности создания пользователя без email')
    def test_creating_user_without_email_error_registration(self, register_new_user_and_return_email_password_name):
        with allure.step('Получение данных нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"password": password, "name": name}

        with allure.step('Попытка регистрации без email'):
            response = requests.post(url=URL_AUTH_REGISTER, data=payload)

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields"
        }

    @allure.step('Проверка невозможности создания пользователя без имени')
    def test_creating_user_without_name_error_registration(self, register_new_user_and_return_email_password_name):
        with allure.step('Получение данных нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"email": email, "password": password}

        with allure.step('Попытка регистрации без имени'):
            response = requests.post(url=URL_AUTH_REGISTER, data=payload)

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields"
        }

    @allure.step('Проверка невозможности создания пользователя без пароля')
    def test_creating_user_without_password_error_registration(self, register_new_user_and_return_email_password_name):
        with allure.step('Получение данных нового пользователя'):
            email, password, name = register_new_user_and_return_email_password_name
            payload = {"email": email, "name": name}

        with allure.step('Попытка регистрации без пароля'):
            response = requests.post(url=URL_AUTH_REGISTER, data=payload)

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields"
        }