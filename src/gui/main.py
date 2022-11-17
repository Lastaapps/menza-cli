from typing import TYPE_CHECKING
from result import Ok, Err
import curses as cr
import time

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW

from src.gui.menu import Menu
from src.gui.info import Info
from src.repo.repo import Repo
from src.repo.repo_impl import RepoImpl

menu_width = 32
info_width = 64

class Main:
    def __init__(
        self,
        repo : Repo = RepoImpl()
    ):
        self.repo = repo

    def exit_courses(self, stdscr: CW):
        cr.nocbreak()
        stdscr.keypad(False)
        cr.echo()
        cr.endwin()
    
    def exit_with_error(self, stdscr: CW, error: Exception):
        self.exit_courses(stdscr)
        print(error)
    
    def run(self, stdscr: CW):
        cr.noecho()
        cr.cbreak()
        cr.curs_set(0)
        stdscr.keypad(True)
    
        size = stdscr.getmaxyx()
        menu_scr = cr.newwin(size[0] - 1, menu_width, 0, 0)
        menu_scr.border()
    
        menu_scr.addstr(0, 3, "CTU Menzas")
        menu_scr.refresh()
    
        menza_list = self.repo.get_menza_list()
        match menza_list:
            case Ok(value):
                menu = Menu(menu_scr, value)
                menu.reload()
            case Err(e):
                self.exit_with_error(stdscr, e)
                return
    
        info_scr = cr.newwin(size[0] - 1, info_width, 0, size[1] - info_width)
        info_scr.border()
    
        info_scr.addstr(0, 3, "Info")
        info_scr.refresh()
    
        info = Info(info_scr)
    
        while True:
            for r in range(1, 7):
                menu.select(r)
                info_data = self.repo.get_complete_info(r)
                match info_data:
                    case Ok(value):
                        info.update_info(value)
                    case Err(e):
                        self.exit_with_error(stdscr, e)

                time.sleep(3)
        input()

        exit_courses(stdscr)
    
    
    def start_app(self):
        cr.wrapper(self.run)
