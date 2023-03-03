"""Abstraction for a view, that can handle key input"""

from abc import ABCMeta, abstractmethod
from enum import Enum

from menza_cli.api.agata_entity import Dish, Subsystem


class HandlerType(Enum):
    """Enum for all the available top level input handling views"""

    MENU = 1
    DISH = 2
    WEEK = 3


class HandlerEvent(metaclass=ABCMeta):
    """Parent for all the available events"""


class Nothing(HandlerEvent):
    """Ignores the key pressed/action already handled"""


class LoadMenza(HandlerEvent):
    """Loads new subsystem"""

    def __init__(self, subsystem: Subsystem):
        self.subsystem = subsystem


class OpenImage(HandlerEvent):
    """Opens the image given in browser"""

    def __init__(self, dish: Dish):
        self.dish = dish


class SwitchToMenu(HandlerEvent):
    """Moves to the menu view"""


class SwitchToDish(HandlerEvent):
    """Moves to the today view"""


class SwitchToWeek(HandlerEvent):
    """Moves to the week view"""


class KeyHandler(metaclass=ABCMeta):
    """Abstraction for a view, that can handle key input"""

    @abstractmethod
    def handle_key(self, char: int) -> HandlerEvent:
        """Lets ancestors handle key input"""
