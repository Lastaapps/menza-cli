from src import di
from . import util
from src.repo.repo import Repo
from result import Ok, Err
from src.api.agata_entity import Subsystem


def print_dish_list(repo: Repo, subsystem: Subsystem) -> None:
    res = repo.get_week_menu(subsystem)
    match res:
        case Ok(value):
            for (_, dishList) in value.items():
                print()
                print(dishList[0].date, dishList[0].day_of_week_name)
                for dish in dishList:
                    print(dish.type_name, dish.weight, dish.name, sep="\t")
        case Err(e):
            print(e)


def command_week(mocked: bool, phrase: str) -> None:
    repo = di.get_repo(mocked)
    menza = util.find_menza(repo, phrase)

    match menza:
        case Ok(value):
            print("Week menu for " + value.description)
            print_dish_list(repo, value)
        case Err(e):
            print(e)
