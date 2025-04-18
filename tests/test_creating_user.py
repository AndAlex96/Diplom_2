import requests
import allure
from app.urls import BASE_URL

@allure.title('Тест создания пользователя')
class TestCreatingUser:

    @allure.step('Проверка создания пользователя с корректными данными')
    def test_creating_new_user_with_correct_date_successful_registration(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email":email, "password":password, "name":name}
        response = requests.post(f'{BASE_URL}api/auth/register', data=payload)
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
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)
        response = requests.post(f'{BASE_URL}api/auth/register', data=payload)
        response_body = response.json()

        assert response.status_code == 403
        assert response_body ==  {
        "success": False,
        "message": "User already exists"
        }

    @allure.step('Проверка невозможности создания пользователя без email')
    def test_creating_user_without_email_error_registration(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)
        response = requests.post(f'{BASE_URL}api/auth/register', data=payload)

        assert response.status_code == 403
        assert response.json() == {
        "success": False,
        "message": "Email, password and name are required fields"
        }

    @allure.step('Проверка невозможности создания пользователя без имени')
    def test_creating_user_without_name_error_registration(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)
        response = requests.post(f'{BASE_URL}api/auth/register', data=payload)

        assert response.status_code == 403
        assert response.json() == {
        "success": False,
        "message": "Email, password and name are required fields"
        }

    @allure.step('Проверка невозможности создания пользователя без пароля')
    def test_creating_user_without_password_error_registration(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)
        response = requests.post(f'{BASE_URL}api/auth/register', data=payload)

        assert response.status_code == 403
        assert response.json() == {
        "success": False,
        "message": "Email, password and name are required fields"
        }