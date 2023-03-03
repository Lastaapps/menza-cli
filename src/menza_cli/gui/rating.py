"""Rating dialog"""

from typing import TYPE_CHECKING

from menza_cli.api.agata_entity import Dish, Subsystem
from menza_cli.repo.repo import Repo

from .key_handler import HandlerEvent, KeyHandler, Nothing

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW


class RatingView(KeyHandler):
    """Rating dialog"""

    def __init__(
        self,
        scr: CW,
        repo: Repo,
        menza: Subsystem,
        dish: Dish,
    ):
        # pylint: disable=E0601

        self.size = scr.getmaxyx()
        self.win = scr
        self.repo = repo
        scr.refresh()

        self.menza = menza
        self.dish = dish

    def handle_key(self, char: int) -> HandlerEvent:
        """Handles user input - just 1 key press"""

        _, width = self.size
        win = self.win
        win.clear()
        win.move(1, 0)
        win.addstr("Working on it...".center(width - 2))
        win.refresh()

        if char in [ord(str(x)) for x in range(1, 6)]:
            self.repo.send_rating(self.menza, self.dish, char - ord("0"))

        return Nothing()

    def draw(self):
        """Redraws itself"""

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
