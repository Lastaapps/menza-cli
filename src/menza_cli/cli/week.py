"""Handles week cli command"""

from result import Err, Ok

from menza_cli import di
from menza_cli.api.agata_entity import Subsystem
from menza_cli.repo.repo import Repo

from . import util


def print_dish_list(repo: Repo, subsystem: Subsystem) -> None:
    """Print week menu for the subsystem"""
    res = repo.get_week_menu(subsystem)
    match res:
        case Ok(value):
            for (_, dish_list) in value.items():
                print()
                print(dish_list[0].date, dish_list[0].day_of_week_name)
                for dish in dish_list:
                    print(dish.type_name, dish.weight, dish.name, sep="\t")
        case Err(error):
            print(error)


def command_week(mocked: bool, phrase: str) -> None:
    """Handles week cli command"""

    repo = di.get_repo(mocked)
    menza = util.find_menza(repo, phrase)

    match menza:
        case Ok(value):
            print(value.description)
            print_dish_list(repo, value)
        case Err(error):
            print(error)
