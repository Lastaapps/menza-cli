"""Show the menza list menu"""

import curses as cr
from typing import TYPE_CHECKING

from menza_cli.api.agata_entity import Subsystem

from .key_handler import HandlerEvent, KeyHandler, LoadMenza, Nothing, SwitchToDish

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW


class MenuView(KeyHandler):
    """Show the menza list menu"""

    def __init__(self, scr: CW):
        # pylint: disable=E0601

        self.index = 0
        self.focused = False
        self.size = scr.getmaxyx()
        self.win = scr
        self.menza_list = []

    def __draw_line(self, index: int):
        """Draws one menza in the list"""

        menza = self.menza_list[index]
        win = self.win
        selected = self.index
        if selected == index:
            win.attron(cr.A_REVERSE if self.focused else cr.A_UNDERLINE)

        text = ("O" if menza.open else "X") + f" {menza.id:2d} " + menza.description
        win.addstr(index, 0, text.ljust(win.getmaxyx()[1]))

        win.attroff(cr.A_REVERSE if self.focused else cr.A_UNDERLINE)

    def __redraw(self):
        """Redraws the whole menu"""

        menza_list = self.menza_list

        for i in range(len(menza_list)):
            self.__draw_line(i)
        self.win.refresh()

    def update_data(self, menza_list: list[Subsystem]):
        """Sets the view with new data"""

        self.menza_list = menza_list
        self.__redraw()

    def __check_index(self) -> None:
        """Checks if index is in bounds"""

        if len(self.menza_list) == 0:
            self.index = 0
            return

        while self.index < 0:
            self.index += len(self.menza_list)

        while self.index >= len(self.menza_list) and len(self.menza_list) != 0:
            self.index -= len(self.menza_list)

    def __select_index(self, index: int):
        """Sets a new index respecting bounds"""

        old_index = self.index
        self.index = index
        self.__check_index()

        self.__draw_line(old_index)
        self.__draw_line(self.index)
        self.win.refresh()

    def handle_key(self, char: int) -> HandlerEvent:
        """Handles keyboard input"""

        if char in (ord("j"), cr.KEY_DOWN):
            self.__select_index(self.index + 1)
            return Nothing()

        if char in (ord("k"), cr.KEY_UP):
            self.__select_index(self.index - 1)
            return Nothing()

        if char in (ord("l"), cr.KEY_RIGHT):
            return SwitchToDish()

        if char in (ord(" "), ord("\n"), ord("o"), cr.KEY_ENTER):
            return LoadMenza(self.menza_list[self.index])

        return Nothing()

    def set_focus(self, focus: bool):
        """
        Registers that it is/is not in focus
        If focused it draws bold lines
        """
        self.focused = focus
        self.__draw_line(self.index)
        self.win.refresh()
