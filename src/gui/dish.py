from typing import TYPE_CHECKING
import curses as cr

from result import Err, Ok

from src.api.agata_entity import Dish, Subsystem
from src.repo.repo import DishRatingMapper, Repo
from .key_handler import (
    HandlerEvent,
    KeyHandler,
    HandlerType,
    Nothing,
    OpenImage,
    SwitchToMenu,
)

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW


class DishView(KeyHandler):
    def __init__(self, scr: CW, repo: Repo):
        self.size = scr.getmaxyx()
        self.win = scr
        self.repo = repo
        scr.refresh()

        self.dish_index = 0
        self.data: dict[str, list[Dish]] = {}
        self.most_allergens = 0
        self.rate_mapper: DishRatingMapper = lambda _, __: (0, 0)
        self.is_showing_image = False

    def __print_image(self, dish: Dish):
        win = self.win
        size = self.size
        win.clear()

        res = self.repo.get_image(dish, size[1], size[0])
        match res:
            case Ok(value):
                win.addstr(value)
            case Err(e):
                win.addstr("Loading image failed\n")
                win.addstr(str(e))

        win.refresh()

    def __get_dish_by_index(self, index: int):
        i = 0
        for value in self.data.values():
            for dish in value:
                if i == index:
                    return dish
                i += 1
        raise RuntimeError("Index out of bounds for dish: " + str(self.dish_index))

    def __get_selected_dish(self):
        return self.__get_dish_by_index(self.dish_index)

    def __is_dish_selected(self, dish: Dish):
        return self.__get_selected_dish() == dish

    def __dish_count(self):
        i = 0
        for value in self.data.values():
            for _ in value:
                i += 1
        return i

    def __select_index(self, new_index: int):
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
        if self.is_showing_image:
            self.__redraw()
            self.is_showing_image = False
            return Nothing()

        if char in [ord("j"), cr.KEY_DOWN]:
            self.__select_index(self.dish_index + 1)
            return Nothing()

        elif char in [ord("k"), cr.KEY_UP]:
            self.__select_index(self.dish_index - 1)
            return Nothing()

        elif char in [ord("h"), cr.KEY_LEFT]:
            return SwitchToMenu()

        # elif char in [ord(' '), ord('\n'), cr.KEY_ENTER]:
        #     self.is_showing_image = False
        #     self.__print_image(self.__get_selected_dish())
        #     return Nothing()

        elif char in [ord("o")]:
            return OpenImage(self.__get_selected_dish())
        else:
            return Nothing()

    def __print_header(self, y: int, label: str) -> None:
        win = self.win
        win.attron(cr.A_UNDERLINE)
        win.addstr(y, 0, label)
        win.attroff(cr.A_UNDERLINE)

    def __print_dish(self, y: int, dish: Dish, selected: bool) -> None:
        win = self.win

        COL_SPACING = 3
        space = " " * COL_SPACING

        name_width = win.getmaxyx()[1] - 3  # offset
        name_width -= 1 + 5  # weight
        name_width -= 12  # price
        name_width -= 8  # rating
        name_width -= 3  # photo
        if self.most_allergens != 0:
            name_width -= self.most_allergens
        else:
            name_width += COL_SPACING  # to compensate
        name_width -= COL_SPACING * 4

        # Weight
        content = dish.weight.rjust(5)
        content += space

        # Name
        if len(dish.complete) <= name_width:
            content += dish.complete.ljust(name_width)
        else:
            content += dish.complete[: name_width - 3] + "..."
        content += space

        # Price
        price = str(int(dish.price_student)).rjust(3) + " / "
        price += str(int(dish.price_normal)).rjust(3) + " 💰"
        content += price
        content += space

        # Rating
        rating = self.rate_mapper(self.subsystem, dish)
        if rating[1] >= 10:
            content += "{:.1f}".format(rating[0]) + "   ⭐"
        elif rating[1] > 0:
            content += "{:.1f}".format(rating[0]) + "(" + str(rating[1]) + ")⭐"
        else:
            content += " " * 8
        content += space

        # Has photo
        content += "📷 " if dish.photo != "" else "   "

        # Allergens
        if self.most_allergens != 0:
            content += ",".join(dish.allergens).rjust(self.most_allergens)
            content += space

        if selected:
            win.attron(cr.A_REVERSE)
        win.addstr(y, 1, content)
        if selected:
            win.attroff(cr.A_REVERSE)

    def __redraw(self) -> None:
        win = self.win
        win.clear()
        data = self.data

        self.most_allergens = 0
        has_values = False
        for value in data.values():
            for dish in value:
                has_values = True
                digits = len(str(dish.allergens)) - 2
                self.most_allergens = max(self.most_allergens, digits)

        if not has_values:
            win.attron(cr.A_REVERSE)
            win.addstr("No dish available")
            win.attroff(cr.A_REVERSE)
            win.refresh()
            return

        line = 0

        for entry in data.items():
            if len(entry[1]) == 0:
                continue

            self.__print_header(line, entry[0])
            line += 1

            for dish in entry[1]:
                selected = self.__is_dish_selected(dish)
                self.__print_dish(line, dish, selected)
                line += 1

            line += 1

        win.refresh()

    def reset(self):
        self.data = {}
        self.dish_index = 0
        win = self.win
        win.clear()
        win.addstr("Loading...")
        win.refresh()

    def update_data(self, subsystem: Subsystem, data: dict[str, list[Dish]]) -> None:
        self.subsystem = subsystem
        self.data = data
        self.__redraw()

    def update_rating(self, mapping: DishRatingMapper):
        self.rate_mapper = mapping
        self.__redraw()
