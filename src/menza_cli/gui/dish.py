"""Main dish list view"""
# Duplicates with week.py - I want them to have the logic separated
# pylint: disable=R0801

import curses as cr
from typing import TYPE_CHECKING

from menza_cli.api.agata_entity import Dish, Subsystem
from menza_cli.repo.repo import DishRatingMapper, Repo

from .key_handler import (
    HandlerEvent,
    KeyHandler,
    Nothing,
    OpenImage,
    SwitchToMenu,
    SwitchToWeek,
)
from .rating import RatingView

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW

COL_SPACING = 3


class DishView(KeyHandler):
    """Main dish view"""

    def __init__(self, scr: CW, repo: Repo):
        # pylint: disable=E0601

        self.size = scr.getmaxyx()
        self.win = scr
        self.repo = repo
        scr.refresh()

        self.dish_index = 0
        self.focused = False
        self.foreground = False
        self.data: dict[str, list[Dish]] = {}
        self.subsystem: Subsystem
        self.most_allergens = 0
        self.rate_mapper: DishRatingMapper = lambda _, __: (0, 0)
        self.is_showing_image = False
        self.rating_view: RatingView | None = None

    # def __print_image(self, dish: Dish):
    #     win = self.win
    #     size = self.size
    #     win.clear()

    #     res = self.repo.get_image(dish, size[1], size[0])
    #     match res:
    #         case Ok(value):
    #             win.addstr(value)
    #         case Err(error):
    #             win.addstr("Loading image failed\n")
    #             win.addstr(str(error))

    #     win.refresh()

    def __get_dish_by_index(self, index: int) -> Dish:
        """Gets a dish by it's index or throws"""

        i = 0
        for value in self.data.values():
            for dish in value:
                if i == index:
                    return dish
                i += 1
        raise RuntimeError("Index out of bounds for dish: " + str(self.dish_index))

    def __get_selected_dish(self) -> Dish:
        """Get's the selected dish"""

        return self.__get_dish_by_index(self.dish_index)

    def __is_dish_selected(self, dish: Dish) -> bool:
        """Checks if the dish is selected"""

        return self.__get_selected_dish() == dish

    def __dish_count(self) -> int:
        """Gets the total number of dishes loaded"""

        i = 0
        for value in self.data.values():
            for _ in value:
                i += 1
        return i

    def __select_index(self, new_index: int) -> None:
        """Selects a dish index, checks bounds and updates screen"""

        count = self.__dish_count()

        if count == 0:
            new_index = 0
        while new_index < 0:
            new_index += count
        while new_index >= count and count != 0:
            new_index -= count

        self.dish_index = new_index
        self.__redraw()

    @staticmethod
    def __inner_scr(scr: CW) -> CW:
        """Gets an inner screen for bordered screen - creates a border"""
        origin = scr.getbegyx()
        size = scr.getmaxyx()
        return cr.newwin(size[0] - 4, size[1] - 4, origin[0] + 2, origin[1] + 2)

    def __open_rating(self) -> None:
        """Opens rating dialog"""

        y, x = self.win.getbegyx()
        height, width = self.size
        rating_width = 41
        rating_height = 7
        rating_border = cr.newwin(
            rating_height,
            rating_width,
            y + (height - rating_height) // 2,
            x + (width - rating_width) // 2,
        )
        rating_border.border()
        rating_border.addstr(0, 3, "Rating")
        rating_border.refresh()
        rating_scr = DishView.__inner_scr(rating_border)
        self.rating_view = RatingView(
            rating_scr, self.repo, self.subsystem, self.__get_selected_dish()
        )
        self.rating_view.draw()

    def handle_key(self, char: int) -> HandlerEvent:
        """Handles key input"""
        # pylint: disable=R0911

        if self.is_showing_image:
            self.__redraw()
            self.is_showing_image = False
            return Nothing()

        if self.rating_view is not None:
            res = self.rating_view.handle_key(char)
            self.rating_view = None
            self.__redraw()
            return res

        if char in [ord("r")]:
            self.__open_rating()
            return Nothing()

        if char in [ord("j"), cr.KEY_DOWN]:
            self.__select_index(self.dish_index + 1)
            return Nothing()

        if char in [ord("k"), cr.KEY_UP]:
            self.__select_index(self.dish_index - 1)
            return Nothing()

        if char in [ord("h"), cr.KEY_LEFT]:
            return SwitchToMenu()

        if char in [ord("w"), cr.KEY_LEFT]:
            return SwitchToWeek()

        # if char in [ord(' '), ord('\n'), cr.KEY_ENTER]:
        #     self.is_showing_image = False
        #     self.__print_image(self.__get_selected_dish())
        #     return Nothing()

        # Same as o for now
        if char in [ord(" "), ord("\n"), cr.KEY_ENTER]:
            return OpenImage(self.__get_selected_dish())

        if char in [ord("o")]:
            return OpenImage(self.__get_selected_dish())

        return Nothing()

    def __print_header(self, y: int, label: str) -> None:
        """Prints category header"""

        win = self.win
        win.attron(cr.A_UNDERLINE)
        win.addstr(y, 0, label)
        win.attroff(cr.A_UNDERLINE)

    def __print_dish(self, y: int, dish: Dish, selected: bool) -> None:
        """Prints a dish line"""
        win = self.win

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
        content = (dish.weight or "").rjust(5)
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
            content += f"{rating[0]:.1f}   ⭐"
        elif rating[1] > 0:
            content += f"{rating[0]:.1f}({str(rating[1])})⭐"
        else:
            content += " " * 8
        content += space

        # Has photo
        content += "📷 " if dish.photo != None else "   "

        # Allergens
        if self.most_allergens != 0:
            content += ",".join([str(x) for x in dish.allergens]).rjust(
                self.most_allergens
            )
            content += space

        if selected and self.focused:
            win.attron(cr.A_REVERSE)
        elif dish.warn:
            win.attron(cr.A_DIM)

        if not dish.active:

            def strike(text: str) -> str:
                # See <https://stackoverflow.com/a/25244576/4039050>
                return "\u0336".join(text) + "\u0336"

            content = strike(content)

        win.addstr(y, 1, content)

        win.attroff(cr.A_REVERSE)
        win.attroff(cr.A_DIM)

    def __redraw(self) -> None:
        if not self.foreground:
            return

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
            if self.focused:
                win.attron(cr.A_REVERSE)
            win.addstr("No dish available")
            if self.focused:
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

    def set_focus(self, focus: bool):
        """Sets teh view focused - selected line is bold"""

        self.focused = focus
        self.__redraw()

    def set_foreground(self, foreground: bool):
        """Puts the view in foreground - it can be redrawn"""

        self.foreground = foreground
        self.__redraw()

    def reset(self):
        """Clears internal state"""

        self.data = {}
        self.dish_index = 0
        win = self.win
        win.clear()
        win.addstr("Loading...")
        win.refresh()

    def update_data(self, subsystem: Subsystem, data: dict[str, list[Dish]]) -> None:
        """Sets the view up with new data set and redraws"""

        self.subsystem = subsystem
        self.data = data
        self.__redraw()

    def update_rating(self, mapping: DishRatingMapper):
        """Sets the view up with a new rating provider and redraws"""
        self.rate_mapper = mapping
        self.__redraw()
