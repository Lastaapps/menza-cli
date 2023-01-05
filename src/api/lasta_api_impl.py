"""Implementation of rating api"""

import base64
from typing import Any

import requests
from cryptography.hazmat.primitives import hashes

from .lasta_api import LastaApi
from .lasta_entity import Rate, Soldout, Statistics, Status


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

    def get_status(self) -> list[Status]:
        """Gets the current rating status"""

        data: list[dict[str, Any]] = self.__request_get("status")

        return [Status(x) for x in data]

    def get_statistics(self) -> Statistics:
        """Gets the current statistics"""

        data: dict[str, Any] = self.__request_get("statistics")

        return Statistics(data)

    def post_rating(self, dish_id: str, rating: int) -> list[Status]:
        """Rates a dish with BE id given"""

        body = Rate(dish_id, rating)
        data = self.__request_post("rate", body)

        return [Status(x) for x in data]

    def post_sold_out(self, dish_id: str) -> list[Status]:
        """Marks a dish with BE id given as sold out"""

        body = Soldout(dish_id)
        data = self.__request_post("sold-out", body)

        return [Status(x) for x in data]

    def dish_id(self, menza_name: str, dish_name: str) -> str:
        """Creates dish id according to BE standard"""

        dish_id = LastaApiImpl.__dish_id("CVUT", menza_name, dish_name)
        # Used for id generation while debugging
        # if "name_part" in dish_name:
        #    raise RuntimeError("id for " + dish_name + ": " + id)

        return dish_id

    @staticmethod
    def __dish_id(provider: str, menza_name: str, dish_name: str) -> str:
        """Creates dish id according to BE standard"""

        dish_id = provider + "_" + menza_name + "_" + dish_name
        digest = hashes.Hash(hashes.SHA1())
        digest.update(dish_id.encode("UTF-8"))

        return base64.b64encode(digest.finalize()).decode("UTF-8")[:8]
