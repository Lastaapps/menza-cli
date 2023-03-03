"""Handles info cli command"""

from result import Err, Ok

from menza_cli import di
from menza_cli.api.agata_entity import Subsystem
from menza_cli.repo.repo import CompleteInfo, Repo

from . import util

# pylint: disable=R0801
# I want to keep the cli format same even when gui format changes


def print_times(info: CompleteInfo) -> None:
    """Prints opening times"""
    for group in info.times.values():

        print(group[0].serving_name)

        for time in group:
            # pylint: disable=C0103
            df = time.day_from
            dt = time.day_to
            tf = time.time_from.rjust(5)
            tt = time.time_to.rjust(5)
            day = df if df == dt or not dt else f"{df} - {dt}"
            hour = tf if tf == tt or not tt else f"{tf} - {tt}"

            text = f"{day.ljust(7)}  {hour.ljust(13)}  {time.from_desc}"
            print(text)
        print()


def print_info(repo: Repo, subsystem: Subsystem) -> None:
    """Print info about the subsystem"""

    data = repo.get_complete_info(subsystem)
    match data:
        case Ok(info):
            if len(info.header) != 0:
                print(info.header, "\n")

            if len(info.footer) != 0:
                print(info.footer, "\n")

            print_times(info)

            for contact in info.contacts:
                if contact.role:
                    print(contact.role)
                if contact.name:
                    print(contact.name)
                if contact.email:
                    print(contact.email)
                if contact.phone:
                    number = contact.phone
                    number = f"+420 {number[0:3]} {number[3:6]} {number[6:9]}"
                    print(number)
                print()

            for address in info.addresses:
                print(address.address)
                print(address.gps)

        case Err(error):
            print(error)


def command_info(mocked: bool, phrase: str) -> None:
    """Handles info cli command"""
    # pylint: disable=R0801

    repo = di.get_repo(mocked)
    menza = util.find_menza(repo, phrase)

    match menza:
        case Ok(value):
            print(value.description)
            print_info(repo, value)
        case Err(error):
            print(error)
