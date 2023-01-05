from abc import ABCMeta, abstractmethod
from enum import Enum
from src.api.agata_entity import Dish, Subsystem


class HandlerType(Enum):
    MENU = 1
    DISH = 2
    WEEK = 3


class HandlerEvent(metaclass=ABCMeta):
    ...


class Nothing(HandlerEvent):
    ...


class LoadMenza(HandlerEvent):
    def __init__(self, subsystem: Subsystem):
        self.subsystem = subsystem


class OpenImage(HandlerEvent):
    def __init__(self, dish: Dish):
        self.dish = dish


class SwitchToMenu(HandlerEvent):
    ...

class SwitchToDish(HandlerEvent):
    ...

class SwitchToWeek(HandlerEvent):
    ...


class KeyHandler(metaclass=ABCMeta):
    @abstractmethod
    def handleKey(self, char: int) -> HandlerEvent:
        pass
