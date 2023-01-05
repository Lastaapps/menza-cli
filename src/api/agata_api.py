from abc import ABCMeta, abstractmethod

from .agata_entity import (
    Address,
    Contact,
    DayDish,
    Dish,
    DishList,
    DishType,
    Info,
    OpenTime,
    ServingPlace,
    Subsystem,
    WeekInfo,
)


class AgataApi(metaclass=ABCMeta):
    @abstractmethod
    def get_dish_list(self) -> list[DishList]:
        """Returns list of dish"""

        pass

    @abstractmethod
    def get_sub_systems(self) -> list[Subsystem]:
        """Gets subsystems"""
        pass

    @abstractmethod
    def get_serving_places(self, subsystem_id: int) -> list[ServingPlace]:
        """Get serving places"""
        pass

    @abstractmethod
    def get_dish_types(self, subsystem_id: int) -> list[DishType]:
        """Gets dish types in a subsystem"""
        pass

    @abstractmethod
    def get_dishes(self, subsystem_id: int) -> list[Dish]:
        """Gets dishes for today in the subsystem given"""
        pass

    @abstractmethod
    def get_info(self, subsystem_id: int) -> list[Info]:
        """Gets info about the subsystem given"""
        pass

    @abstractmethod
    def get_open_times(self, subsystem_id: int) -> list[OpenTime]:
        """Gets opening times of the subsystem given"""
        pass

    @abstractmethod
    def get_contact(self) -> list[Contact]:
        """Gets contacts to the subsystem given"""
        pass

    @abstractmethod
    def get_address(self) -> list[Address]:
        """Gets address of the subsystem given"""
        pass

    @abstractmethod
    def get_week_info(self, subsystem_id: int) -> list[WeekInfo]:
        """Gets week dish menus available"""
        pass

    @abstractmethod
    def get_day_dish(self, week_id: int) -> list[DayDish]:
        """Gets a dish menu for the week id given"""
        pass

    @abstractmethod
    def get_image_url(self, subsystem_id: int, name: str) -> str:
        """Gets URL of the given name"""
        pass
