from abc import ABCMeta, abstractmethod
from typing import Callable

from result import Result

from src.api.agata_entity import (
    Address,
    Contact,
    DayDish,
    Dish,
    Info,
    OpenTime,
    Subsystem,
)

TimeServingGroup = dict[int, list[OpenTime]]
TimeGroup = dict[int, TimeServingGroup]
DishRatingMapper = Callable[
    [Subsystem, Dish], tuple[float, int]
]  # (rating, rating count)


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
    def get_week_menu(
        self, system: Subsystem
    ) -> Result[dict[str, list[DayDish]], Exception]:
        """Get week dish menu in a menza"""
        pass

    @abstractmethod
    def get_complete_info(
        self, subsystem: Subsystem
    ) -> Result[CompleteInfo, Exception]:
        """Combines all the info about a menza"""
        pass

    @abstractmethod
    def get_rating(self) -> Result[DishRatingMapper, Exception]:
        """Get the current rating status"""
        pass

    @abstractmethod
    def get_image(self, dish: Dish, width: int, height: int) -> Result[str, Exception]:
        """Gets image in ascii_art format"""
        pass

    @abstractmethod
    def get_image_url(self, dish: Dish) -> str | None:
        """Gets image web url"""
        pass

    @abstractmethod
    def send_rating(
        self, subsystem: Subsystem, dish: Dish, rating: int
    ) -> Result[None, Exception]:
        """Send rating for dish"""
        pass
