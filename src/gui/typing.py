from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW
