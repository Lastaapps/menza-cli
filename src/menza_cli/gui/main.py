"""The main gui handler"""

import curses as cr

# import subprocess
import webbrowser
from typing import TYPE_CHECKING

from result import Err, Ok

from menza_cli.api.agata_entity import Subsystem
from menza_cli.gui.dish import DishView
from menza_cli.gui.info import InfoView
from menza_cli.gui.menu import MenuView
from menza_cli.gui.week import WeekView
from menza_cli.repo.repo import Repo

from .key_handler import (
    HandlerEvent,
    HandlerType,
    LoadMenza,
    Nothing,
    OpenImage,
    SwitchToDish,
    SwitchToMenu,
    SwitchToWeek,
)

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW

MENU_WIDTH = 32
INFO_WIDTH = 40
MIN_TERM_WIDTH = 150
MIN_TERM_HEIGHT = 42


class Main:
    """The main gui handler"""

    def __init__(self, repo: Repo):
        self.repo = repo
        self.input_state = HandlerType.MENU

        self.stdscr: CW
        self.menu_view: MenuView
        self.dish_view: DishView
        self.week_view: WeekView
        self.info_view: InfoView

    def exit_courses(self):
        """Exits ncurses"""
        cr.nocbreak()
        cr.echo()
        cr.endwin()
        self.stdscr.keypad(False)

    def exit_with_message(self, message: str):
        """Shows an error message, awaits key press and exits"""
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
        """Shows an error message, awaits key press and exits"""
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
        """Creates a screen inside another (pads borders)"""
        # pylint: disable=E0601

        origin = scr.getbegyx()
        size = scr.getmaxyx()
        return cr.newwin(size[0] - 4, size[1] - 4, origin[0] + 2, origin[1] + 2)

    def __layout_screen(self, stdscr: CW):
        """Lays all the view on screen"""

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
        self.menu_view = MenuView(menu_scr)

        # Draw dish list border
        dish_width = size[1] - MENU_WIDTH - INFO_WIDTH
        dish_border = cr.newwin(size[0] - 1, dish_width, 0, MENU_WIDTH)
        dish_border.border()
        dish_border.addstr(0, 3, "Dish list")
        dish_border.refresh()
        dish_scr = Main.__inner_scr(dish_border)
        self.dish_view = DishView(dish_scr, self.repo)
        week_scr = Main.__inner_scr(dish_border)
        self.week_view = WeekView(week_scr, self.repo)

        # Draw info border
        info_border = cr.newwin(size[0] - 1, INFO_WIDTH, 0, size[1] - INFO_WIDTH)
        info_border.border()
        # Add the info section label
        info_border.addstr(0, 3, "Info")
        info_border.refresh()
        info_scr = Main.__inner_scr(info_border)
        self.info_view = InfoView(info_scr)

        stdscr.move(size[0] - 1, 0)
        stdscr.addstr(
            "Developed by Lasta Apps (Petr Laštovička) in 2022/23."
            + " "
            + "Monty Pythons are great, Python not so much."
        )
        github = "Please award me with a star at https://github.com/Lastaapps/menza-cli"
        stdscr.move(size[0] - 1, size[1] - 1 - len(github))
        stdscr.addstr(github)

    def __setup_rating(self):
        """Sets rating up"""

        rating = self.repo.get_rating()
        match rating:
            case Ok(value):
                self.dish_view.update_rating(value)
            case Err(_):
                pass

    def __setup_subsystems(self):
        """Loads the menza list"""

        menza_list = self.repo.get_menza_list()
        menu_view = self.menu_view

        match menza_list:
            case Ok(value):
                menu_view.update_data(value)
                menu_view.set_focus(True)
                return True
            case Err(error):
                self.exit_with_error(error)
                return False

    def __load_subsystem(self, subsystem: Subsystem):
        """Loads data for the subsystem given"""

        dish_view = self.dish_view
        week_view = self.week_view
        info_view = self.info_view

        dish_data = self.repo.get_dish_list(subsystem)
        week_data = self.repo.get_week_menu(subsystem)
        info_data = self.repo.get_complete_info(subsystem)

        match dish_data:
            case Ok(value):
                dish_view.update_data(subsystem, value)
            case Err(error):
                self.exit_with_error(error)
                return False

        match week_data:
            case Ok(value):
                week_view.update_data(subsystem, value)
            case Err(error):
                self.exit_with_error(error)
                return False

        match info_data:
            case Ok(value):
                info_view.update_info(value)
            case Err(error):
                self.exit_with_error(error)
                return False
        return True

    def __handle_input(self) -> None:
        """Handles a key input, delegates it to the current view"""

        stdscr = self.stdscr

        while True:
            char = stdscr.getch()

            if char == cr.ERR:
                continue

            if char in (ord("q"), 27):
                return

            res: HandlerEvent
            match self.input_state:
                case HandlerType.MENU:
                    res = self.menu_view.handle_key(char)
                case HandlerType.DISH:
                    res = self.dish_view.handle_key(char)
                case HandlerType.WEEK:
                    res = self.week_view.handle_key(char)
                case _:
                    raise RuntimeError("Unknown key type: " + str(self.input_state))

            # matching handling result
            if isinstance(res, Nothing):
                pass

            elif isinstance(res, LoadMenza):
                self.menu_view.set_focus(False)
                self.dish_view.set_focus(True)
                self.week_view.set_focus(False)
                self.input_state = HandlerType.DISH
                self.dish_view.reset()
                self.week_view.reset()
                if not self.__load_subsystem(res.subsystem):
                    return
                self.week_view.set_foreground(False)
                self.dish_view.set_foreground(True)

            elif isinstance(res, OpenImage):
                url = self.repo.get_image_url(res.dish)
                if isinstance(url, str):
                    # Opens tab twice for some reasong
                    webbrowser.open_new_tab(url)
                    # subprocess.run(
                    #     ["xdg-open", url],
                    #     stdout=subprocess.DEVNULL,
                    #     stderr=subprocess.DEVNULL,
                    # )

            elif isinstance(res, SwitchToMenu):
                self.menu_view.set_focus(True)
                self.dish_view.set_focus(False)
                self.week_view.set_focus(False)
                self.input_state = HandlerType.MENU

            elif isinstance(res, SwitchToDish):
                self.menu_view.set_focus(False)
                self.dish_view.set_focus(True)
                self.week_view.set_focus(False)
                self.week_view.set_foreground(False)
                self.dish_view.set_foreground(True)
                self.input_state = HandlerType.DISH

            elif isinstance(res, SwitchToWeek):
                self.menu_view.set_focus(False)
                self.dish_view.set_focus(False)
                self.week_view.set_focus(True)
                self.dish_view.set_foreground(False)
                self.week_view.set_foreground(True)
                self.input_state = HandlerType.WEEK

            else:
                raise RuntimeError(
                    "Unhandled type returned from key handling: " + str(type(res))
                )

    def __run(self, stdscr: CW):
        """Prepares all the bits"""

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
        self.__handle_input()

        self.exit_courses()

    def start_app(self):
        """Starts ncurses wrapper and the whole app"""
        cr.wrapper(self.__run)
