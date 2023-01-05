"""Handles dish cli command"""

from result import Err, Ok

from src import di
from src.api.agata_entity import Subsystem
from src.repo.repo import Repo

from . import util


def print_dish_list(repo: Repo, subsystem: Subsystem) -> None:
    """Prints dish menu for the subsystem given"""

    res = repo.get_dish_list(subsystem)
    match res:
        case Ok(value):
            for (_, dish_list) in value.items():
                for dish in dish_list:
                    print(
                        dish.weight,
                        dish.name,
                        dish.price_student,
                        dish.price_normal,
                        ",".join(dish.allergens),
                        sep="\t",
                    )
        case Err(error):
            print(error)


def command_dish(mocked: bool, phrase: str) -> None:
    """Handles dish cli command"""
    # pylint: disable=R0801

    repo = di.get_repo(mocked)
    menza = util.find_menza(repo, phrase)

    match menza:
        case Ok(value):
            print(value.description)
            print_dish_list(repo, value)
        case Err(error):
            print(error)
