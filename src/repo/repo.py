from abc import ABCMeta, abstractmethod
from result import Result
import ascii_magic

from src.api.agata_api import AgataApi
from src.api.agata_api_impl import AgataApiImpl
import src.api.lasta_api as lasta
from src.api.agata_entity import Info, OpenTime, Contact, Address
from src.api.agata_entity import Subsystem, Dish

TimeServingGroup = dict[int, list[OpenTime]]
TimeGroup = dict[int, TimeServingGroup]


class CompleteInfo:
    def __init__(
        self,
        info: Info,
        openTimes: TimeServingGroup,
        contacts: list[Contact],
        addresses: list[Address],
    ):
        self.header = info.header
        self.footer = info.footer
        self.times = openTimes
        self.contacts = contacts
        self.addresses = addresses


class Repo(metaclass=ABCMeta):
    def __init__(self, agata_api: AgataApi = AgataApiImpl()):
        self.agata_api = agata_api

    @abstractmethod
    def get_menza_list(self) -> Result[list[Subsystem], Exception]:
        """Gets list of all the CTU menzas"""
        pass

    @abstractmethod
    def get_dish_list(
        self, system: Subsystem
    ) -> Result[dict[str, list[Dish]], Exception]:
        """Get today dish menu in a menza"""
        pass

    @abstractmethod
    def get_complete_info(
        self, subsystem: Subsystem
    ) -> Result[CompleteInfo, Exception]:
        """Combines all the info about a menza"""
        pass

    @abstractmethod
    def get_image(self, dish: Dish) -> Result[ascii_magic.AsciiArt, Exception]:
        """Gets image in ascii_art format"""
        pass
