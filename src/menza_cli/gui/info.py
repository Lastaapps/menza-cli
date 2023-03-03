"""Shows info about a subsystem"""

from typing import TYPE_CHECKING

from menza_cli.repo.repo import CompleteInfo

if TYPE_CHECKING:
    from _curses import _CursesWindow as CW
    from _curses import error as crerror
else:
    from typing import Any as CW


class InfoView:
    """Shows info about a subsystem"""

    def __init__(self, scr: CW):
        # pylint: disable=E0601

        self.size = scr.getmaxyx()
        self.win = scr

    # def __print_label(self, win: CW, pos: int, label: str):
    #     """Prints a header of a footer, returns number of lines to skip"""
    #     if len(label) != 0:
    #         win.addstr(pos, 0, label)
    #         return pos + len(label) // win.getmaxyx()[1] + 2 + label.count("\n")
    #     return pos

    def __print_times(self, info: CompleteInfo) -> None:
        """Prints opening times"""
        win = self.win

        for group in info.times.values():

            win.addstr(group[0].serving_name)
            win.addstr("\n")

            for time in group:
                # pylint: disable=C0103
                df = time.day_from
                dt = time.day_to
                tf = (time.time_from or "").rjust(5)
                tt = (time.time_to or "").rjust(5)
                day = (df if df == dt or not dt else f"{df} - {dt}") or ""
                hour = (tf if tf == tt or not tt else f"{tf} - {tt}") or ""
                description = time.from_desc or ""

                text = f"{day.ljust(7)}  {hour.ljust(13)}  {description}"
                win.addstr(text)
                win.addstr("\n")
            win.addstr("\n")

    def update_info(self, info: CompleteInfo) -> None:
        """Sets the view up with new info and redraws it"""

        win = self.win
        # may crash if text overflows
        try:
            win.clear()

            if info.header:
                win.addstr(info.header + "\n\n")
            if info.footer:
                win.addstr(info.footer + "\n\n")

            self.__print_times(info)

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
                    number = contact.phone
                    number = f"+420 {number[0:3]} {number[3:6]} {number[6:9]}"
                    win.addstr(number)
                    win.addstr("\n")
                win.addstr("\n")

            for address in info.addresses:
                win.addstr(address.address)
                win.addstr("\n")
                win.addstr(address.gps)
                win.addstr("\n")
        finally:
            win.refresh()
