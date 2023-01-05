"""Rating api abstraction"""

from abc import ABCMeta, abstractmethod

from .lasta_entity import Statistics, Status


class LastaApi(metaclass=ABCMeta):
    """Rating api abstraction"""

    @abstractmethod
    def get_status(self) -> list[Status]:
        """Gets the current rating status"""

    @abstractmethod
    def get_statistics(self) -> Statistics:
        """Gets the current statistics"""

    @abstractmethod
    def post_rating(self, dish_id: str, rating: int) -> list[Status]:
        """Rates a dish with BE id given"""

    @abstractmethod
    def post_sold_out(self, dish_id: str) -> list[Status]:
        """Marks a dish with BE id given as sold out"""

    @abstractmethod
    def dish_id(self, menza_name: str, dish_name: str) -> str:
        """Creates dish id according to BE standard"""
