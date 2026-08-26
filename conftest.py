import threading
import time
import json
import random
import string
import pytest
import allure
from fake_api import app
from api_client import CourierAPIClient


# --- Существующая фикстура (НЕ МЕНЯЕТСЯ) ---
@pytest.fixture(scope="session")
def fake_server():
    """Запускает fake_api на порту 5001."""
    server_thread = threading.Thread(
        target=app.run,
        kwargs={"port": 5001, "debug": False, "use_reloader": False},
        daemon=True,
    )
    server_thread.start()
    time.sleep(0.5)
    yield


# --- НОВЫЕ фикстуры для изоляции тестов ---

@pytest.fixture(scope="session")
def client(fake_server):
    """Создаёт клиент для API."""
    base_url = "http://127.0.0.1:5001/api"
    token = "test_token_123"
    return CourierAPIClient(base_url, token)


@pytest.fixture
def unique_courier_data():
    """Создаёт уникальные данные для курьера."""
    phone = "+79" + ''.join(random.choices(string.digits, k=9))

    return {
        "first_name": "Иван",
        "last_name": "Петров",
        "phone": phone
    }


@pytest.fixture
def created_courier(client, unique_courier_data):
    """
    Создаёт курьера через API и удаляет его после теста.
    Важно: используется try/finally для гарантированной очистки.
    """
    response = client.create_courier(unique_courier_data)
    courier_id = response["id"]

    yield courier_id, unique_courier_data

    # Очистка после теста — даже если тест упал
    try:
        client.delete_courier(courier_id)
    except Exception as e:
        print(f"Ошибка при удалении курьера {courier_id}: {e}")


# --- НОВЫЙ Allure-хук для автоматических вложений при падении ---

...
