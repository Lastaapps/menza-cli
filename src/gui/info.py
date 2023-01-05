from typing import TYPE_CHECKING

from src.repo.repo import CompleteInfo

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
    from _curses import error as crerror
else:
    from typing import Any as CW


class Info:
    def __init__(self, scr: CW):
        self.size = scr.getmaxyx()
        self.win = scr

    def _print_label(self, win: CW, pos: int, label: str):
        if len(label) != 0:
            win.addstr(pos, 0, label)
            return pos + len(label) // win.getmaxyx()[1] + 2 + label.count("\n")
        return pos

    def update_info(self, info: CompleteInfo) -> None:
        win = self.win
        # may crash if text overflows
        try:
            win.clear()

            win.addstr(info.header + "\n\n") if info.header else ...
            win.addstr(info.footer + "\n\n") if info.footer else ...
            win.refresh()

            for group in info.times.values():

                win.addstr(group[0].serving_name)
                win.addstr("\n")

                for time in group:
                    df = time.day_from
                    dt = time.day_to
                    tf = time.time_from.rjust(5)
                    tt = time.time_to.rjust(5)
                    day = df if df == dt or not dt else f"{df} - {dt}"
                    hour = tf if tf == tt or not tt else f"{tf} - {tt}"

                    text = f"{day.ljust(7)}  {hour.ljust(13)}  {time.from_desc}"
                    win.addstr(text)
                    win.addstr("\n")
                win.addstr("\n")

            for contact in info.contacts:
                if contact.role:
                    win.addstr(contact.role)
                    win.addstr("\n")
                if contact.name:
                    win.addstr(contact.name)
                    win.addstr("\n")
                if contact.email:
                    win.addstr(contact.email)
                    win.addstr("\n")
                if contact.phone:
                    n = contact.phone
                    number = f"+420 {n[0:3]} {n[3:6]} {n[6:9]}"
                    win.addstr(number)
                    win.addstr("\n")
                win.addstr("\n")

            for address in info.addresses:
                win.addstr(address.address)
                win.addstr("\n")
                win.addstr(address.gps)
                win.addstr("\n")
        except (Exception):
            pass

        win.refresh()
