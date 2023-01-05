from typing import TYPE_CHECKING
import curses as cr

from result import Err, Ok

from src.api.agata_entity import DayDish, Subsystem
from src.repo.repo import DishRatingMapper, Repo
from .key_handler import (
    HandlerEvent,
    KeyHandler,
    Nothing,
    OpenImage,
    SwitchToMenu,
    SwitchToDish,
)
from .rating import RatingView

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW


class WeekView(KeyHandler):
    def __init__(self, scr: CW, repo: Repo):
        self.size = scr.getmaxyx()
        self.win = scr
        self.repo = repo
        scr.refresh()

        self.dish_index = 0
        self.focused = False
        self.foreground = False
        self.data: dict[str, list[DayDish]] = {}
        self.longest_type_name = 0

    def __get_dish_by_index(self, index: int) -> DayDish:
        i = 0
        for value in self.data.values():
            for dish in value:
                if i == index:
                    return dish
                i += 1
        raise RuntimeError("Index out of bounds for dish: " + str(self.dish_index))

    def __get_selected_dish(self) -> DayDish:
        return self.__get_dish_by_index(self.dish_index)

    def __is_dish_selected(self, dish: DayDish) -> bool:
        return self.__get_selected_dish() == dish

    def __dish_count(self) -> int:
        i = 0
        for value in self.data.values():
            for _ in value:
                i += 1
        return i

    def __select_index(self, new_index: int) -> None:
        count = self.__dish_count()

        if count == 0:
            new_index = 0
        while new_index < 0:
            new_index += count
        while new_index >= count and count != 0:
            new_index -= count

        self.dish_index = new_index
        self.__redraw()

    def handleKey(self, char: int) -> HandlerEvent:

        if char in [ord("j"), cr.KEY_DOWN]:
            self.__select_index(self.dish_index + 1)
            return Nothing()

        elif char in [ord("k"), cr.KEY_UP]:
            self.__select_index(self.dish_index - 1)
            return Nothing()

        elif char in [ord("h"), cr.KEY_LEFT]:
            return SwitchToMenu()

        elif char in [ord("w"), cr.KEY_LEFT]:
            return SwitchToDish()

        else:
            return Nothing()

    def __print_header(self, y: int, label: str) -> None:
        win = self.win
        win.attron(cr.A_UNDERLINE)
        win.addstr(y, 0, label)
        win.attroff(cr.A_UNDERLINE)

    def __print_dish(self, y: int, dish: DayDish, selected: bool) -> None:
        win = self.win

        COL_SPACING = 3
        space = " " * COL_SPACING

        name_width = win.getmaxyx()[1] - 3  # offset
        name_width -= 1 + 5  # weight
        if self.longest_type_name != 0:
            name_width -= self.longest_type_name
        else:
            name_width += COL_SPACING  # to compensate
        name_width -= COL_SPACING * 2

        content = ""

        # Type
        content += dish.type_name.ljust(self.longest_type_name)
        content += space

        # Weight
        content += dish.weight.rjust(5)
        content += space

        # Name
        if len(dish.name) <= name_width:
            content += dish.name.ljust(name_width)
        else:
            content += dish.name[: name_width - 3] + "..."
        content += space

        if selected and self.focused:
            win.attron(cr.A_REVERSE)

        win.addstr(y, 1, content)

        win.attroff(cr.A_REVERSE)

    def __redraw(self) -> None:
        if not self.foreground:
            return

        win = self.win
        win.clear()
        data = self.data

        self.longest_type_name = 0
        has_values = False
        for value in data.values():
            for dish in value:
                has_values = True
                digits = len(dish.type_name)
                self.longest_type_name = max(self.longest_type_name, digits)

        if not has_values:
            if self.focused:
                win.attron(cr.A_REVERSE)
            win.addstr("No week menu available")
            if self.focused:
                win.attroff(cr.A_REVERSE)
            win.refresh()
            return

        line = 0

        for entry in data.items():
            if len(entry[1]) == 0:
                continue

            first = entry[1][0]
            self.__print_header(line, first.date + " " + first.day_of_week_name)
            line += 1

            for dish in entry[1]:
                selected = self.__is_dish_selected(dish)
                self.__print_dish(line, dish, selected)
                line += 1

            line += 1

        win.refresh()

    def set_focus(self, focus: bool):
        self.focused = focus
        self.__redraw()

    def set_foreground(self, foreground: bool):
        self.foreground = foreground
        self.__redraw()

    def reset(self):
        self.data = {}
        self.dish_index = 0
        win = self.win
        win.clear()
        win.addstr("Loading...")
        win.refresh()

    def update_data(self, subsystem: Subsystem, data: dict[str, list[DayDish]]) -> None:
        self.subsystem = subsystem
        self.data = data
        self.__redraw()
