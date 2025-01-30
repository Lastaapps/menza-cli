"""Implementation of rating api"""

from typing import Any

import requests

from .lasta_api import LastaApi
from .lasta_entity import Rate, Statistics, Status


class LastaApiImpl(LastaApi):
    """Implementation of rating api"""

    def __init__(self, url: str, api_key: str):
        self.base_url = url
        self.api_key = api_key

    def __build_url(self, endpoint: str) -> str:
        """Adds the last path argumrnt to the base url"""

        return self.base_url + "/api/v1/" + endpoint

    def __request_get(self, path: str) -> Any:
        """Performs GET request to the path given"""

        headers = {"X-Api-Key": self.api_key}

        response: requests.Response = requests.get(
            self.__build_url(path),
            headers=headers,
            timeout=5,
        )

        return response.json()

    def __request_post(self, path: str, data: Any) -> Any:
        """Performs POST request to the path given, sends the data as JSON"""

        headers = {"X-Api-Key": self.api_key}

        response: requests.Response = requests.post(
            self.__build_url(path),
            json=data.__dict__,
            headers=headers,
            timeout=5,
        )

        return response.json()

    def __api_menza_id(self, menza_id: str) -> str:
        return f"CTU_{menza_id}"

    def get_status(self, menza_id: str) -> list[Status]:
        """Gets the current rating status"""

        data: list[dict[str, Any]] = self.__request_get(
            f"status/{self.__api_menza_id(menza_id)}"
        )

        return [Status(x) for x in data]

    def get_statistics(self) -> Statistics:
        """Gets the current statistics"""

        data: dict[str, Any] = self.__request_get("statistics")

        return Statistics(data)

    def post_rating(
        self, menza_id: str, dish_id: str, dish_name: str, rating: int
    ) -> list[Status]:
        """Rates a dish with BE id given"""

        body = Rate(dish_id, dish_name, rating)
        data = self.__request_post(f"rate/{self.__api_menza_id(menza_id)}", body)

        return [Status(x) for x in data]
