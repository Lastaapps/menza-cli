from typing import TYPE_CHECKING
from src.api.agata_entity import Subsystem
from .key_handler import (
    HandlerEvent,
    KeyHandler,
    HandlerType,
    LoadMenza,
    Nothing,
    SwitchToDish,
)
import curses as cr

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW


class Menu(KeyHandler):
    def __init__(self, scr: CW):
        self.index = 0
        self.size = scr.getmaxyx()
        self.win = scr
        self.menza_list = []

    def draw_line(self, index: int):
        menza = self.menza_list[index]
        win = self.win
        selected = self.index
        if selected == index:
            win.attron(cr.A_REVERSE)
        text = ("O" if menza.open else "X") + f" {menza.id:2d} " + menza.description
        win.addstr(index, 0, text.ljust(win.getmaxyx()[1]))
        win.attroff(cr.A_REVERSE)

    def update_data(self, menza_list: list[Subsystem]):
        self.menza_list = menza_list

        for i in range(len(menza_list)):
            self.draw_line(i)
        self.win.refresh()

    def __check_index(self) -> None:
        if len(self.menza_list) == 0:
            self.index = 0
            return

        while self.index < 0:
            self.index += len(self.menza_list)

        while self.index >= len(self.menza_list) and len(self.menza_list) != 0:
            self.index -= len(self.menza_list)

    def __select_index(self, index: int):
        old_index = self.index
        self.index = index
        self.__check_index()

        self.draw_line(old_index)
        self.draw_line(self.index)
        self.win.refresh()

    def handleKey(self, char: int) -> HandlerEvent:
        if char in (ord("j"), cr.KEY_DOWN):
            self.__select_index(self.index + 1)
            return Nothing()

        elif char in (ord("k"), cr.KEY_UP):
            self.__select_index(self.index - 1)
            return Nothing()

        elif char in (ord("l"), cr.KEY_RIGHT):
            return SwitchToDish()

        elif char in (ord(" "), ord("\n"), cr.KEY_ENTER):
            return LoadMenza(self.menza_list[self.index])
        else:
            return Nothing()
