from typing import TYPE_CHECKING
import curses as cr

from src.api.agata_entity import Dish, Subsystem
from src.repo.repo import DishRatingMapper

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW


class DishView:
    def __init__(self, scr: CW):
        self.size = scr.getmaxyx()
        self.win = scr
        scr.refresh()
        self.data: dict[str, list[Dish]] = {}
        self.most_allergens = 0
        self.rate_mapper : DishRatingMapper = lambda _, __: (0, 0)

    def __print_header(self, y: int, label: str) -> None:
        win = self.win
        win.attron(cr.A_UNDERLINE)
        win.addstr(y, 0, label)
        win.attroff(cr.A_UNDERLINE)

    def __print_dish(self, y: int, dish: Dish, selected: bool) -> None:
        win = self.win

        COL_SPACING = 3
        space = " " * COL_SPACING

        name_width = win.getmaxyx()[1]
        name_width -= 1 + 5  # weight
        name_width -= 12  # price
        name_width -= 8 # rating
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
        if (rating[1] >= 10):
            content += "{:.1f}".format(rating[0]) + "   ⭐"
        elif (rating[1] > 0):
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

        win.addstr(y, 1, content)

    def __redraw(self) -> None:
        win = self.win
        win.clear()
        data = self.data

        if not data:
            win.addstr(0, 0, "No dish available")
            win.refresh()
            return

        self.most_allergens = 0
        for value in data.values():
            for dish in value:
                digits = len(str(dish.allergens)) - 2
                self.most_allergens = max(self.most_allergens, digits)

        line = 0

        for entry in data.items():
            if len(entry[1]) == 0:
                continue

            self.__print_header(line, entry[0])
            line += 1

            for dish in entry[1]:
                self.__print_dish(line, dish, False)
                line += 1

            line += 1

        win.refresh()

    def update_data(self, subsystem: Subsystem, data: dict[str, list[Dish]]) -> None:
        self.subsystem = subsystem
        self.data = data
        self.__redraw()

    def update_rating(self, mapping: DishRatingMapper):
        self.rate_mapper = mapping
        self.__redraw()
