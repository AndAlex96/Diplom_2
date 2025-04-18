from app.urls import BASE_URL
import requests
import allure

@allure.title('Тест изменения данных пользователя')
class TestChangeDataUser:

    @allure.step('Проверка изменения авторизованным пользователем email')
    def test_change_email_user_with_authorization_successful_cheng(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)

        payload_auth = {"email": email, "password": password}
        response_auth = requests.post(f'{BASE_URL}api/auth/login', payload_auth)
        response_auth_json = response_auth.json()
        token_auth = response_auth_json.get('accessToken')

        payload_change_data = {"email": f'1{email}'}
        response_change_data = requests.patch(f'{BASE_URL}api/auth/user', data=payload_change_data, headers={'Authorization':token_auth})
        response_change_data_json = response_change_data.json()

        assert response_change_data.status_code == 200
        assert response_change_data_json ==  {"success": True,
            "user": {
            "email": f'1{email}',
            "name": name}
                                              }

    @allure.step('Проверка изменения авторизованным пользователем имени')
    def test_change_name_user_with_authorization_successful_cheng(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)

        payload_auth = {"email": email, "password": password}
        response_auth = requests.post(f'{BASE_URL}api/auth/login', payload_auth)
        response_auth_json = response_auth.json()
        token_auth = response_auth_json.get('accessToken')

        payload_change_data = {"name": f'1{name}'}
        response_change_data = requests.patch(f'{BASE_URL}api/auth/user', data=payload_change_data, headers={'Authorization':token_auth})
        response_change_data_json = response_change_data.json()

        assert response_change_data.status_code == 200
        assert response_change_data_json ==  {"success": True,
            "user": {
            "email": email,
            "name": f'1{name}'}
                                              }

    @allure.step('Проверка изменения авторизованным пользователем пароля')
    def test_change_password_user_with_authorization_successful_cheng(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)

        payload_auth = {"email": email, "password": password}
        response_auth = requests.post(f'{BASE_URL}api/auth/login', payload_auth)
        response_auth_json = response_auth.json()
        token_auth = response_auth_json.get('accessToken')

        payload_change_data = {"password": f'1{password}'}
        response_change_data = requests.patch(f'{BASE_URL}api/auth/user', data=payload_change_data, headers={'Authorization':token_auth})
        response_change_data_json = response_change_data.json()

        assert response_change_data.status_code == 200
        assert response_change_data_json ==  {"success": True,
            "user": {
            "email": email,
            "name": name}
                                              }

    @allure.step('Проверка изменения неавторизованным пользователем email')
    def test_change_email_user_without_authorization_successful_cheng(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)

        payload_change_data = {"email": f'1{email}'}
        response_change_data = requests.patch(f'{BASE_URL}api/auth/user', data=payload_change_data)
        response_change_data_json = response_change_data.json()

        assert response_change_data.status_code == 401
        assert response_change_data_json == {
            "success": False,
            "message": "You should be authorised"
        }

    @allure.step('Проверка изменения неавторизованным пользователем имени')
    def test_change_name_user_without_authorization_successful_cheng(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)

        payload_change_data = {"name": f'1{name}'}
        response_change_data = requests.patch(f'{BASE_URL}api/auth/user', data=payload_change_data)
        response_change_data_json = response_change_data.json()

        assert response_change_data.status_code == 401
        assert response_change_data_json == {
            "success": False,
            "message": "You should be authorised"
        }

    @allure.step('Проверка изменения неавторизованным пользователем пароля')
    def test_change_password_user_without_authorization_successful_cheng(self, register_new_user_and_return_email_password_name):
        email, password, name = register_new_user_and_return_email_password_name
        payload = {"email": email, "password": password, "name": name}
        requests.post(f'{BASE_URL}api/auth/register', data=payload)

        payload_change_data = {"password": f'1{password}'}
        response_change_data = requests.patch(f'{BASE_URL}api/auth/user', data=payload_change_data)
        response_change_data_json = response_change_data.json()

        assert response_change_data.status_code == 401
        assert response_change_data_json == {
            "success": False,
            "message": "You should be authorised"
        }