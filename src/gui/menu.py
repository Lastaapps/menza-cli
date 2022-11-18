from typing import TYPE_CHECKING
from src.api.agata_entity import Subsystem
import curses as cr

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW


class Menu:
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
        text = ("O" if menza.open else "X") + f" {menza.id} " + menza.description
        win.addstr(index, 0, text.ljust(win.getmaxyx()[1]))
        win.attroff(cr.A_REVERSE)

    def update_data(self, menza_list: list[Subsystem]):
        self.menza_list = menza_list

        for i in range(len(menza_list)):
            self.draw_line(i)
        self.win.refresh()

    def select(self, subsystem: Subsystem):
        index = self.menza_list.index(subsystem)
        old_index = self.index
        self.index = index
        self.draw_line(old_index)
        self.draw_line(index)
        self.win.refresh()
