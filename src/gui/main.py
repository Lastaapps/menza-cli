from typing import TYPE_CHECKING
import curses as cr
import time
import random
from src.gui.menu import Menu
from src.gui.info import Info
from src.repo import repo

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW

menu_width = 32
info_width = 64


def exit_courses(stdscr: CW):
    cr.nocbreak()
    stdscr.keypad(False)
    cr.echo()
    cr.endwin()


def run(stdscr: CW):
    cr.noecho()
    cr.cbreak()
    cr.curs_set(0)
    stdscr.keypad(True)

    size = stdscr.getmaxyx()
    menu_scr = cr.newwin(size[0] - 1, menu_width, 0, 0)
    menu_scr.border()

    menu_scr.addstr(0, 3, "CTU Menzas")
    menu_scr.refresh()

    menza_list = repo.get_menza_list()
    menu = Menu(menu_scr, menza_list)
    menu.reload()

    info_scr = cr.newwin(size[0] - 1, info_width, 0, size[1] - info_width)
    info_scr.border()

    info_scr.addstr(0, 3, "Info")
    info_scr.refresh()

    info = Info(info_scr)

    while True:
        for r in range(1, 7):
            menu.select(r)
            info.update_info(repo.get_complete_info(r))
            time.sleep(3)
    input()

    exit_courses(stdscr)


def start_app():
    cr.wrapper(run)
