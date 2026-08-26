import requests


class CourierAPIClient:
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.auth_token = auth_token

    def _get_auth_header(self):
        if not self.auth_token:
            raise ValueError("AUTH_TOKEN не задан")
        return {"Authorization": f"Bearer {self.auth_token}"}

    def get_courier_by_id(self, courier_id: int):
        url = f"{self.base_url}/couriers/{courier_id}"
        headers = self._get_auth_header()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def create_courier(self, data: dict):
        url = f"{self.base_url}/couriers"
        headers = self._get_auth_header()
        headers["Content-Type"] = "application/json"
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def update_courier(self, courier_id: int, data: dict):
        """Обновляет данные курьера (частичное обновление)."""
        url = f"{self.base_url}/couriers/{courier_id}"
        headers = self._get_auth_header()
        headers["Content-Type"] = "application/json"
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete_courier(self, courier_id: int):
        url = f"{self.base_url}/couriers/{courier_id}"
        headers = self._get_auth_header()
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()