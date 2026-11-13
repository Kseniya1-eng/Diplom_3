import random
import string

import requests

from data.urls import REGISTER_ENDPOINT, USER_ENDPOINT


def generate_random_string(length: int = 8) -> str:
    """Генерирует случайную строку."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_unique_email() -> str:
    """Генерирует уникальный email."""
    return f'ui_{generate_random_string(10)}@yandex.ru'


def create_user_via_api() -> dict:
    """Создаёт пользователя через API и возвращает email, password, name, token."""
    payload = {
        'email': generate_unique_email(),
        'password': generate_random_string(10),
        'name': generate_random_string(6),
    }
    response = requests.post(REGISTER_ENDPOINT, json=payload)
    response.raise_for_status()
    return {
        'email': payload['email'],
        'password': payload['password'],
        'name': payload['name'],
        'token': response.json().get('accessToken'),
    }


def delete_user_via_api(token: str):
    """Удаляет пользователя через API по токену."""
    if token:
        requests.delete(USER_ENDPOINT, headers={'Authorization': token})
