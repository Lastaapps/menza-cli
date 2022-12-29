from typing import Optional, Any
import requests

from .agata_entity import (
    DishList,
    Subsystem,
    ServingPlace,
    DishType,
    Dish,
    Info,
    OpenTime,
    Contact,
    Address,
    WeekInfo,
    DayDish,
)
from .agata_api import AgataApi

# TODO move into config
g_base_url: str = "https://agata.suz.cvut.cz"
g_api_path: str = "/jidelnicky/JAPI/json_API.php"
g_api_key: str = "v1XiWjvD"


class AgataApiImpl(AgataApi):
    def __init__(
        self,
        base_url: str = g_base_url,
        api_path: str = g_api_path,
        api_key: str = g_api_key,
    ):
        """Create api object to get data from BE"""

        self.base_url = base_url
        self.api_path = api_path
        self.api_key = api_key

    def __build_url(
        self,
        function: str,
        subsystem: Optional[int] = None,
        secondId: Optional[int] = None,
    ) -> str:
        """Builds request URL"""

        url: str = self.base_url + self.api_path + "?api=" + self.api_key
        url += "&Funkce=" + function
        if subsystem != None:
            url += "&Podsystem=" + str(subsystem)
        if secondId != None:
            url += "&SecondID=" + str(secondId)
        return url

    def __parse_response_body(self, url: str) -> Any:
        """Decodes resulting JSON"""

        r: requests.Response = requests.get(url)
        return r.json()

    def get_dish_list(self) -> list[DishList]:
        """Returns list of dish"""

        data: list[dict[str, Any]] = self.__parse_response_body(
            self.__build_url("GetJidelnicky")
        )
        return [DishList(x) for x in data]

    def get_sub_systems(self) -> list[Subsystem]:
        """Gets subsystems"""

        data: list[dict[str, Any]] = (
            self.__parse_response_body(self.__build_url("GetPodsystemy", secondId=1)) or []
        )
        return [Subsystem(x) for x in data]

    def get_serving_places(self, subsystem_id: int) -> list[ServingPlace]:
        """Get serving places"""

        data: list[dict[str, Any]] = (
            self.__parse_response_body(self.__build_url("GetVydejny", subsystem_id)) or []
        )
        return [ServingPlace(x) for x in data]

    def get_dish_types(self, subsystem_id: int) -> list[DishType]:
        """Gets dish types in a subsystem"""

        data: list[dict[str, Any]] = (
            self.__parse_response_body(self.__build_url("GetKategorie", subsystem_id)) or []
        )
        return [DishType(x) for x in data]

    def get_dishes(self, subsystem_id: int) -> list[Dish]:
        """Gets dishes for today in the subsystem given"""

        data: list[dict[str, Any]] = (
            self.__parse_response_body(self.__build_url("GetJidla", subsystem_id, 1)) or []
        )
        return [Dish(x) for x in data]

    def get_info(self, subsystem_id: int) -> list[Info]:
        """Gets info about the subsystem given"""

        data: list[dict[str, Any]] = (
            self.__parse_response_body(self.__build_url("GetInfo", subsystem_id, 1)) or []
        )
        return [Info(x) for x in data]

    def get_open_times(self, subsystem_id: int) -> list[OpenTime]:
        """Gets opening times of the subsystem given"""

        data: list[dict[str, Any]] = (
            self.__parse_response_body(self.__build_url("GetOtDoby", subsystem_id, 1)) or []
        )
        return [OpenTime(x) for x in data]

    def get_contact(self) -> list[Contact]:
        """Gets contacts to the subsystem given"""

        data: list[dict[str, Any]] = (
            self.__parse_response_body(self.__build_url("GetKontakty")) or []
        )
        return [Contact(x) for x in data]

    def get_address(self) -> list[Address]:
        """Gets address of the subsystem given"""

        data: list[dict[str, Any]] = (
            self.__parse_response_body(self.__build_url("GetAdresy")) or []
        )
        return [Address(x) for x in data]

    def get_week_info(self, subsystem_id: int) -> list[WeekInfo]:
        """Gets week dish menus available"""

        data: list[dict[str, Any]] = (
            self.__parse_response_body(self.__build_url("GetTydny", subsystem_id)) or []
        )
        return [WeekInfo(x) for x in data]

    def get_day_dish(self, week_id: int) -> list[DayDish]:
        """Gets a dish menu for the week id given"""

        data: list[dict[str, Any]] = (
            self.__parse_response_body(self.__build_url("GetTydnyDny", secondId=week_id))
            or []
        )
        return [DayDish(x) for x in data]

    def get_image_url(self, subsystem_id: int, name: str) -> str:
        """Gets URL of the given name"""

        return (
            self.base_url
            + f"/jidelnicky/showfoto.php?clPodsystem={subsystem_id}&xFile={name}"
        )
