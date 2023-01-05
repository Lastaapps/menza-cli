from src import di
from src.repo.repo import Repo
from . import util
from result import Ok, Err
from src.api.agata_entity import Subsystem


def print_info(repo: Repo, subsystem: Subsystem) -> None:
    data = repo.get_complete_info(subsystem)
    match data:
        case Ok(info):
            if len(info.header) != 0:
                print(info.header, "\n")

            if len(info.footer) != 0:
                print(info.footer, "\n")

            for group in info.times.values():

                print(group[0].serving_name)

                for time in group:
                    df = time.day_from
                    dt = time.day_to
                    tf = time.time_from.rjust(5)
                    tt = time.time_to.rjust(5)
                    day = df if df == dt or not dt else f"{df} - {dt}"
                    hour = tf if tf == tt or not tt else f"{tf} - {tt}"

                    text = f"{day.ljust(7)}  {hour.ljust(13)}  {time.from_desc}"
                    print(text)
                print()

            for contact in info.contacts:
                if contact.role:
                    print(contact.role)
                if contact.name:
                    print(contact.name)
                if contact.email:
                    print(contact.email)
                if contact.phone:
                    n = contact.phone
                    number = f"+420 {n[0:3]} {n[3:6]} {n[6:9]}"
                    print(number)
                print()

            for address in info.addresses:
                print(address.address)
                print(address.gps)

        case Err(e):
            print(e)


def command_info(mocked: bool, phrase: str) -> None:
    repo = di.get_repo(mocked)
    menza = util.find_menza(repo, phrase)

    match menza:
        case Ok(value):
            print("Info for " + value.description)
            print_info(repo, value)
        case Err(e):
            print(e)
