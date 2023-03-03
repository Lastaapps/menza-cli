"""Abstraction for data flow management"""

from abc import ABCMeta, abstractmethod
from typing import Any, Callable

from result import Result

# pylint: disable=R0913

from menza_cli.api.agata_entity import (
    Address,
    Contact,
    DayDish,
    Dish,
    Info,
    News,
    OpenTime,
    Subsystem,
)

TimeServingGroup = dict[int, list[OpenTime]]
TimeGroup = dict[int, TimeServingGroup]
DishRatingMapper = Callable[
    [Subsystem, Dish], tuple[float, int]
]  # (rating, rating count)


class CompleteInfo:
    """
    Holds combined info about a subsystem
    Headers, open times, contacts, address
    """

    def __init__(
        self,
        info: Info,
        news: News,
        open_times: TimeServingGroup,
        contacts: list[Contact],
        addresses: list[Address],
    ):
        self.header = news.header
        self.footer = info.footer
        self.times = open_times
        self.contacts = contacts
        self.addresses = addresses

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    def __eq__(self, obj: Any):
        return isinstance(obj, CompleteInfo) and obj.__dict__ == self.__dict__


class Repo(metaclass=ABCMeta):
    """Abstraction for data flow management"""

    @abstractmethod
    def get_menza_list(self) -> Result[list[Subsystem], Exception]:
        """Gets list of all the CTU menzas"""

    @abstractmethod
    def get_dish_list(
        self, system: Subsystem
    ) -> Result[dict[str, list[Dish]], Exception]:
        """Get today dish menu in a menza"""

    @abstractmethod
    def get_week_menu(
        self, system: Subsystem
    ) -> Result[dict[str, list[DayDish]], Exception]:
        """Get week dish menu in a menza"""

    @abstractmethod
    def get_complete_info(
        self, subsystem: Subsystem
    ) -> Result[CompleteInfo, Exception]:
        """Combines all the info about a menza"""

    @abstractmethod
    def get_rating(self) -> Result[DishRatingMapper, Exception]:
        """Get the current rating status"""

    # @abstractmethod
    # def get_image(self, dish: Dish, width: int, height: int) -> Result[str, Exception]:
    #     """Gets image in ascii_art format"""

    @abstractmethod
    def get_image_url(self, dish: Dish) -> str | None:
        """Gets image web url"""

    @abstractmethod
    def send_rating(
        self, subsystem: Subsystem, dish: Dish, rating: int
    ) -> Result[None, Exception]:
        """Send rating for dish"""
