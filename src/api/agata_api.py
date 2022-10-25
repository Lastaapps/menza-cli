from typing import Optional, Any
import requests
from src.api.agata_entity import *

# TODO move into config
api_key :str = "v1XiWjvD"
base_url: str = "https://agata-new.suz.cvut.cz/jidelnicky/JAPI/json_API.php"

def build_url(
    function: str,
    subsystem: Optional[int] = None,
    secondId: Optional[int] = None,
) -> str:
    url: str = base_url + "?api=" + api_key
    url += "&Funkce=" + function
    if subsystem != None:
        url += "&Podsystem=" + str(subsystem)
    if secondId != None:
        url += "&SecondID=" + str(secondId)
    return url

def parse_response_body(url: str) -> Any:
    r: requests.Response = requests.get(url)
    return r.json()

def get_dish_list() -> list[DishList]:
    data :list[dict[str, Any]] = parse_response_body(build_url("GetJidelnicky"))
    return [DishList(x) for x in data]
    
def get_sub_systems() -> list[Subsystem]:
    data :list[dict[str, Any]] = parse_response_body(build_url("GetPodsystemy"))
    return [Subsystem(x) for x in data]

def get_serving_places(subsystem_id: int) -> list[ServingPlace]:
    data :list[dict[str, Any]] = parse_response_body(build_url("GetVydejny", subsystem_id))
    return [ServingPlace(x) for x in data]

def get_dish_types(subsystem_id: int) -> list[DishType]:
    data :list[dict[str, Any]] = parse_response_body(build_url("GetKategorie", subsystem_id))
    return [DishType(x) for x in data]

def get_dishes(subsystem_id: int) -> list[Dish]:
    data :list[dict[str, Any]] = parse_response_body(build_url("GetJidelnicky", subsystem_id, 1))
    return [Dish(x) for x in data]

def get_info(subsystem_id: int) -> list[Info]:
    data :list[dict[str, Any]] = parse_response_body(build_url("GetInfo", subsystem_id, 1))
    return [Info(x) for x in data]

def from_times(subsystem_id: int) -> list[OpenTime]:
    data :list[dict[str, Any]] = parse_response_body(build_url("GetOtDoby", subsystem_id, 1))
    return [OpenTime(x) for x in data]

def get_contact() -> list[Contact]:
    data :list[dict[str, Any]] = parse_response_body(build_url("GetKontakty"))
    return [Contact(x) for x in data]

def get_address() -> list[Address]:
    data :list[dict[str, Any]] = parse_response_body(build_url("GetAdresy"))
    return [Address(x) for x in data]

def get_week_info(subsystem_id: int) -> WeekInfo:
    data :dict[str, Any] = parse_response_body(build_url("GetTydny", subsystem_id))
    return WeekInfo(data)

def get_day_dish(week_id: int) -> list[DayDish]:
    data :list[dict[str, Any]] = parse_response_body(build_url("GetTydnyDny", secondId=week_id))
    return [DayDish(x) for x in data]
