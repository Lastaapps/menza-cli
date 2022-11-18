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
from src.gui.dish import DishView
from src.repo.repo import Repo
from src.repo.repo_impl import RepoImpl
from src.api.agata_entity import Subsystem

MENU_WIDTH = 32
INFO_WIDTH = 40
MIN_TERM_WIDTH = 150
MIN_TERM_HEIGHT = 42


class Main:
    def __init__(self, repo: Repo = RepoImpl()):
        self.repo = repo

    def exit_courses(self):
        cr.nocbreak()
        cr.echo()
        cr.endwin()
        self.stdscr.keypad(False)

    def exit_with_error(self, error: Exception):
        self.exit_courses()
        print(error)

    @staticmethod
    def __inner_scr(scr: CW) -> CW:
        xy = scr.getbegyx()
        size = scr.getmaxyx()
        return cr.newwin(size[0] - 4, size[1] - 4, xy[0] + 2, xy[1] + 2)

    def __layout_screen(self, stdscr: CW):
        cr.noecho()
        cr.cbreak()
        cr.curs_set(0)
        stdscr.keypad(True)
        size = stdscr.getmaxyx()

        # Draw menu border
        menu_border = cr.newwin(size[0] - 1, MENU_WIDTH, 0, 0)
        menu_border.border()
        # Add app name into the border
        menu_border.addstr(0, 3, "CTU Menzas")
        menu_border.refresh()
        menu_scr = Main.__inner_scr(menu_border)
        self.menu_view = Menu(menu_scr)

        # Draw dish list border
        dish_width = size[1] - MENU_WIDTH - INFO_WIDTH
        dish_border = cr.newwin(size[0] - 1, dish_width, 0, MENU_WIDTH)
        dish_border.border()  # TODO add pretty corners
        dish_border.addstr(0, 3, "Dish list")
        dish_border.refresh()
        dish_scr = Main.__inner_scr(dish_border)
        self.dish_view = DishView(dish_scr)

        # Draw info border
        info_border = cr.newwin(size[0] - 1, INFO_WIDTH, 0, size[1] - INFO_WIDTH)
        info_border.border()
        # Add the info section label
        info_border.addstr(0, 3, "Info")
        info_border.refresh()
        info_scr = Main.__inner_scr(info_border)
        self.info_view = Info(info_scr)

    def __run_with_subsystems(self, menza_list: list[Subsystem]):

        menu_view = self.menu_view
        dish_view = self.dish_view
        info_view = self.info_view

        menu_view.update_data(menza_list)

        system = list(filter(lambda s: "Strahov" in s.description, menza_list))[0]
        menu_view.select(system)

        info_data = self.repo.get_complete_info(system)

        match info_data:
            case Ok(value):
                info_view.update_info(value)
            case Err(e):
                self.exit_with_error(e)

        res = self.repo.get_dish_list(system)
        match res:
            case Ok(value):
                dish_view.update_info(value)
            case Err(e):
                self.exit_with_error(e)

        input()

        while True:
            for system in menza_list:
                menu_view.select(system)

                info_data = self.repo.get_complete_info(system)

                match info_data:
                    case Ok(value):
                        info_view.update_info(value)
                    case Err(e):
                        self.exit_with_error(e)

                res = self.repo.get_dish_list(system)
                match res:
                    case Ok(value):
                        dish_view.update_info(value)
                    case Err(e):
                        self.exit_with_error(e)

                time.sleep(1)

    def run(self, stdscr: CW):
        self.stdscr = stdscr

        # Check screen size
        if stdscr.getmaxyx()[1] < MIN_TERM_WIDTH:
            self.exit_courses()
            print(
                f"Your term is to small, width must be at least {MIN_TERM_WIDTH} is required"
            )
            return
        if stdscr.getmaxyx()[0] < MIN_TERM_HEIGHT:
            self.exit_courses()
            print(
                f"Your term is to small, height must be at least {MIN_TERM_HEIGHT} is required"
            )
            return

        self.__layout_screen(stdscr)

        menza_list = self.repo.get_menza_list()
        match menza_list:
            case Ok(value):
                self.__run_with_subsystems(value)
            case Err(e):
                self.exit_with_error(e)
                return

        self.exit_courses(stdscr)

    def start_app(self):
        cr.wrapper(self.run)
