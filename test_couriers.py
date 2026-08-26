import os
import pytest
import requests
from dotenv import load_dotenv
from api_client import CourierAPIClient
from models import CourierModel

load_dotenv()


@pytest.fixture(scope="session")
def client():
    base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:5001/api")
    token = os.getenv("AUTH_TOKEN", "test_token_123")
    return CourierAPIClient(base_url, token)


@pytest.fixture
def new_courier_data():
    return {
        "first_name": "Мария",
        "last_name": "Сидорова",
        "phone": "+79997654321"
    }


@pytest.mark.usefixtures("fake_server")
class TestCourierClient:

    # --- Позитивные тесты ---

    def test_get_courier_by_id(self, client):
        """Получение курьера — проверка через pydantic-модель."""
        courier = client.get_courier_by_id(1)
        validated = CourierModel(**courier)
        assert validated.id == 1
        assert validated.first_name == "Иван"

    def test_create_courier(self, client, new_courier_data):
        """Создание курьера — проверка через pydantic-модель."""
        result = client.create_courier(new_courier_data)
        validated = CourierModel(**result)
        assert validated.first_name == "Мария"

    def test_update_courier(self, client):
        """Обновление имени курьера."""
        updated = client.update_courier(1, {"first_name": "Пётр"})
        assert updated["first_name"] == "Пётр"

    def test_delete_courier(self, client):
        """Удаление курьера и проверка, что он больше не доступен."""
        client.delete_courier(2)
        with pytest.raises(requests.exceptions.HTTPError):
            client.get_courier_by_id(2)

    # --- Негативные тесты ---

    def test_create_courier_without_required_field(self, client):
        """Создание без first_name — ошибка 400."""
        with pytest.raises(requests.exceptions.HTTPError):
            client.create_courier({"last_name": "Безымянный"})

    def test_update_nonexistent_courier(self, client):
        """Обновление несуществующего курьера — ошибка 404."""
        with pytest.raises(requests.exceptions.HTTPError):
            client.update_courier(99999, {"first_name": "Призрак"})