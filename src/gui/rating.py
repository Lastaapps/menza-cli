from typing import TYPE_CHECKING

from result import Err, Ok
from src.repo.repo import Repo
from src.api.agata_entity import Subsystem, Dish
from .key_handler import (
    HandlerEvent,
    KeyHandler,
    Nothing,
    OpenImage,
    SwitchToMenu,
)

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW


class RatingView(KeyHandler):
    def __init__(
        self,
        scr: CW,
        repo: Repo,
        menza: Subsystem,
        dish: Dish,
    ):
        self.size = scr.getmaxyx()
        self.win = scr
        self.repo = repo
        scr.refresh()

        self.menza = menza
        self.dish = dish

    def handleKey(self, char: int) -> HandlerEvent:
        self.win.clear()
        self.win.refresh()

        if char in [ord(str(x)) for x in range(1, 6)]:
            self.repo.send_rating(self.menza, self.dish, char - ord("0"))

        return Nothing()

    def draw(self):
        win = self.win
        win.clear()

        _, width = self.size
        name = self.dish.name

        if len(name) <= width - 2:
            name = name.center(width - 2)
        else:
            name = name[: width - 2 - 3] + "..."

        win.move(0, 0)
        win.addstr(name)
        win.move(1, 0)
        win.addstr("Enter rating from 1 to 5".center(width - 2))
        win.move(2, 0)
        win.addstr("Or anything else to exit".center(width - 2))

        win.refresh()
