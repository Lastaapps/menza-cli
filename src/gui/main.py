from typing import TYPE_CHECKING
from result import Ok, Err
import curses as cr
import webbrowser
import subprocess

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
from .key_handler import (
    HandlerType,
    HandlerEvent,
    Nothing,
    LoadMenza,
    OpenImage,
    SwitchToDish,
    SwitchToMenu,
)

MENU_WIDTH = 32
INFO_WIDTH = 40
MIN_TERM_WIDTH = 150
MIN_TERM_HEIGHT = 42


class Main:
    def __init__(self, repo: Repo = RepoImpl()):
        self.repo = repo
        self.input_state = HandlerType.MENU

    def exit_courses(self):
        cr.nocbreak()
        cr.echo()
        cr.endwin()
        self.stdscr.keypad(False)

    def exit_with_message(self, message: str):
        stdscr = self.stdscr
        stdscr.clear()

        stdscr.addstr("App failed with an exception.\n\n")
        stdscr.addstr(
            str(message) + "\n\n",
        )
        stdscr.addstr("Press a key to exit...")
        stdscr.refresh()

        stdscr.getch()

    def exit_with_error(self, error: Exception):
        stdscr = self.stdscr
        stdscr.clear()

        stdscr.addstr("App failed with an exception.\n\n")
        stdscr.addstr(
            str(error) + "\n\n",
        )
        stdscr.addstr("Press a key to exit...")
        stdscr.refresh()

        stdscr.getch()

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
        self.dish_view = DishView(dish_scr, self.repo)

        # Draw info border
        info_border = cr.newwin(size[0] - 1, INFO_WIDTH, 0, size[1] - INFO_WIDTH)
        info_border.border()
        # Add the info section label
        info_border.addstr(0, 3, "Info")
        info_border.refresh()
        info_scr = Main.__inner_scr(info_border)
        self.info_view = Info(info_scr)

    def __setup_rating(self):
        rating = self.repo.get_rating()
        match rating:
            case Ok(value):
                self.dish_view.update_rating(value)
            case Err(_):
                pass

    def __setup_subsystems(self):

        menza_list = self.repo.get_menza_list()
        menu_view = self.menu_view

        match menza_list:
            case Ok(value):
                menu_view.update_data(value)
                menu_view.setFocus(True)
                return True
            case Err(e):
                self.exit_with_error(e)
                return False

    def __load_subsystem(self, subsystem: Subsystem):

        dish_view = self.dish_view
        info_view = self.info_view

        dish_data = self.repo.get_dish_list(subsystem)
        info_data = self.repo.get_complete_info(subsystem)

        match dish_data:
            case Ok(value):
                dish_view.update_data(subsystem, value)
            case Err(e):
                self.exit_with_error(e)
                return False

        match info_data:
            case Ok(value):
                info_view.update_info(value)
            case Err(e):
                self.exit_with_error(e)
                return False
        return True

    def __handleInput(self) -> None:
        stdscr = self.stdscr
        while True:
            char = stdscr.getch()

            if char == cr.ERR:
                continue
            elif char in (ord("q"), 27):
                return

            res: HandlerEvent
            match self.input_state:
                case HandlerType.MENU:
                    res = self.menu_view.handleKey(char)
                case HandlerType.DISH:
                    res = self.dish_view.handleKey(char)
                case _:
                    raise RuntimeError("Unknown key type: " + str(self.input_state))

            # matching handling result
            if isinstance(res, Nothing):
                ...

            elif isinstance(res, LoadMenza):
                self.menu_view.setFocus(False)
                self.dish_view.setFocus(True)
                self.input_state = HandlerType.DISH
                self.dish_view.reset()
                if not self.__load_subsystem(res.subsystem):
                    return

            elif isinstance(res, OpenImage):
                url = self.repo.get_image_url(res.dish)
                if isinstance(url, str):
                    # Opens tab twice for some reasong
                    # webbrowser.open_new_tab(url)
                    subprocess.run(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            elif isinstance(res, SwitchToMenu):
                self.menu_view.setFocus(True)
                self.dish_view.setFocus(False)
                self.input_state = HandlerType.MENU

            elif isinstance(res, SwitchToDish):
                self.menu_view.setFocus(False)
                self.dish_view.setFocus(True)
                self.input_state = HandlerType.DISH

            else:
                raise RuntimeError(
                    "Unhandled type returned from key handling: " + str(type(res))
                )

    def __run(self, stdscr: CW):
        self.stdscr = stdscr
        stdscr.refresh()

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

        if not self.__setup_subsystems():
            return

        self.__setup_rating()  # may fail, not a huge problem

        # handle keyboard
        self.__handleInput()

        self.exit_courses()

    def start_app(self):
        cr.wrapper(self.__run)
