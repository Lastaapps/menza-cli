from typing import TYPE_CHECKING
from src.api.agata_entity import Subsystem
import curses as cr

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW


class Menu:
    def __init__(self, scr: CW, menza_list: list[Subsystem]):
        self.index = 0
        xy = scr.getbegyx()
        size = scr.getmaxyx()
        inner = cr.newwin(size[0] - 2, size[1] - 2, xy[0] + 1, xy[1] + 1)
        self.win = inner
        self.menza_list = menza_list

    def draw_line(self, index: int):
        menza = self.menza_list[index]
        win = self.win
        selected = self.index
        if selected == index:
            win.attron(cr.A_REVERSE)
        text = ("O" if menza.open else "X") + f" {menza.id} " + menza.description
        win.addstr(index, 1, text.ljust(win.getmaxyx()[1] - 1))
        win.attroff(cr.A_REVERSE)

    def reload(self):
        for i in range(len(self.menza_list)):
            self.draw_line(i)
        self.win.refresh()

    def select(self, index: int):
        old_index = self.index
        self.index = index
        self.draw_line(old_index)
        self.draw_line(index)
        self.win.refresh()
