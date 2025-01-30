"""Rating api abstraction"""

from abc import ABCMeta, abstractmethod

from .lasta_entity import Statistics, Status


class LastaApi(metaclass=ABCMeta):
    """Rating api abstraction"""

    @abstractmethod
    def get_status(self, menza_id: str) -> list[Status]:
        """Gets the current rating status"""

    @abstractmethod
    def get_statistics(self) -> Statistics:
        """Gets the current statistics"""

    @abstractmethod
    def post_rating(
        self, menza_id: str, dish_id: str, dish_name: str, rating: int
    ) -> list[Status]:
        """Rates a dish with BE id given"""
