from app.helpers.auxiliary_functions import generate_email_password_name
from app.urls import BASE_URL
import requests
import pytest

@pytest.fixture
def register_new_user_and_return_email_password_name():
    return generate_email_password_name()

@pytest.fixture
def delete_all_data_after_test(register_new_user_and_return_email_password_name):
    email, password, name = register_new_user_and_return_email_password_name
    yield
    payload_for_auth = {"email":email, "name":name}
    response = requests.post(f'{BASE_URL}api/auth/token', data=payload_for_auth)
    response_json = response.json()
    payload_for_del = response_json.get('accessToken')
    requests.delete(f'{BASE_URL}api/auth/user', data=payload_for_del)
