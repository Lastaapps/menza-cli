from abc import ABCMeta, abstractmethod

from .lasta_entity import *


class LastaApi(metaclass=ABCMeta):
    @abstractmethod
    def get_status(self) -> list[Status]:
        """Gets the current rating status"""
        pass

    @abstractmethod
    def get_statistics(self) -> Statistics:
        """Gets the current statistics"""
        pass

    @abstractmethod
    def post_rating(self, id: str, rating: int) -> list[Status]:
        """Rates a dish with BE id given"""
        pass

    @abstractmethod
    def post_sold_out(self, id: str) -> list[Status]:
        """Marks a dish with BE id given as sold out"""
        pass

    @abstractmethod
    def dish_id(self, menza_name: str, dish_name: str) -> str:
        """Creates dish id according to BE standard"""
        pass
