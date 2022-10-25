from typing import Any
import requests
from src.api.lasta_entity import *
from cryptography.hazmat.primitives import hashes

# TODO move into config
api_key :str = "menza-cli_15becd42-cbae-48b2-aa69-650d06763454"
base_url: str = "https://lastaapps.sh.cvut.cz/menza"

def build_url(
    endpoint: str
) -> str:
    return base_url + "/api/v1/" + endpoint

def request_get(url: str) -> Any:
    headers = { "X-Api-Key" : api_key }
    r: requests.Response = requests.get(url, headers = headers)
    return r.json()

def request_post(url: str, data: Any) -> Any:
    headers = { "X-Api-Key" : api_key }
    r: requests.Response = requests.post(url, data = data.__dict__, headers = headers)
    return r.json()

def get_status() -> list[Status]:
    data:list[dict[str, Any]] = request_get("status")
    return [Status(x) for x in data]

def get_statistics() -> Statistics:
    data :dict[str, Any] = request_get("statistics")
    return Statistics(data)

def post_rating(id: str, rating: int) -> None:
    data = Rate(id, rating)
    request_post("rate", data)

def post_sold_out(id: str) -> None:
    data = Soldout(id)
    request_post("sold-out", data)

def dish_id(menza_name: str, dish_name: str) -> str:
    return __dish_id("CVUT", menza_name, dish_name)

def __dish_id(provider: str, menza_name: str, dish_name: str) -> str:
    id = provider + "_" + menza_name + "_" + dish_name
    digest = hashes.Hash(hashes.SHA1())
    digest.update(str.encode(id))
    return digest.finalize().decode()[:8]
