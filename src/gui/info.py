from typing import TYPE_CHECKING
import curses as cr
from src.repo.repo import CompleteInfo

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
else:
    from typing import Any as CW


class Info:
    def __init__(self, scr: CW):
        xy = scr.getbegyx()
        size = scr.getmaxyx()
        inner = cr.newwin(size[0] - 2, size[1] - 2, xy[0] + 1, xy[1] + 1)
        self.win = inner

    def _print_label(self, win: CW, pos: int, label: str):
        if len(label) != 0:
            win.addstr(pos, 0, label)
            return pos + len(label) // win.getmaxyx()[1] + 2 + label.count("\n")
        return pos

    def update_info(self, info: CompleteInfo):
        win = self.win
        win.clear()

        pos: int = 0

        pos = self._print_label(win, pos, info.header)
        pos = self._print_label(win, pos, info.footer)

        for group in info.times.values():
            win.addstr(pos, 0, group[0].serving_name)
            pos += 1
            for time in group:
                df = time.day_from
                dt = time.day_to
                tf = time.time_from.rjust(5)
                tt = time.time_to.rjust(5)
                day = df if df == dt or not dt else f"{df} - {dt}"
                hour = tf if tf == tt or not tt else f"{tf} - {tt}"

                text = f"{day.ljust(7)}  {hour.ljust(13)}  {time.from_desc}"
                win.addstr(pos, 0, text)
                pos += 1
            pos += 1

        for contact in info.contacts:
            if contact.role:
                win.addstr(pos, 0, contact.role)
                pos += 1
            if contact.name:
                win.addstr(pos, 0, contact.name)
                pos += 1
            if contact.email:
                win.addstr(pos, 0, contact.email)
                pos += 1
            if contact.phone:
                n = contact.phone
                number = f"+420 {n[0:3]} {n[3:6]} {n[6:9]}"
                win.addstr(pos, 0, number)
                pos += 1
            pos += 1

        for address in info.addresses:
            win.addstr(pos, 0, address.address)
            pos += 1
            win.addstr(pos, 0, address.gps)
            pos += 2

        win.refresh()
