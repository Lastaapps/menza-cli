from typing import Any
import requests
from src.api.lasta_entity import *
from cryptography.hazmat.primitives import hashes
import base64

# TODO move into config
api_key: str = "menza-cli_15becd42-cbae-48b2-aa69-650d06763454"
base_url: str = "https://lastaapps.sh.cvut.cz/menza"


def build_url(endpoint: str) -> str:
    return base_url + "/api/v1/" + endpoint


def request_get(url: str) -> Any:
    requests.packages.urllib3.util.connection.HAS_IPV6 = False
    headers = {"X-Api-Key": api_key}
    r: requests.Response = requests.get(build_url(url), headers=headers)
    return r.json()


def request_post(url: str, data: Any) -> Any:
    requests.packages.urllib3.util.connection.HAS_IPV6 = False
    headers = {"X-Api-Key": api_key}
    r: requests.Response = requests.post(
        build_url(url), json=data.__dict__, headers=headers
    )
    return r.json()


def get_status() -> list[Status]:
    data: list[dict[str, Any]] = request_get("status")
    return [Status(x) for x in data]


def get_statistics() -> Statistics:
    data: dict[str, Any] = request_get("statistics")
    return Statistics(data)


def post_rating(id: str, rating: int) -> list[Status]:
    body = Rate(id, rating)
    data = request_post("rate", body)
    return [Status(x) for x in data]


def post_sold_out(id: str) -> list[Status]:
    body = Soldout(id)
    data = request_post("sold-out", body)
    return [Status(x) for x in data]


def dish_id(menza_name: str, dish_name: str) -> str:
    return __dish_id("CVUT", menza_name, dish_name)


def __dish_id(provider: str, menza_name: str, dish_name: str) -> str:
    id = provider + "_" + menza_name + "_" + dish_name
    digest = hashes.Hash(hashes.SHA256())
    digest.update(id.encode("UTF-8"))
    return base64.b64encode(digest.finalize()).decode("UTF-8")[:8]
