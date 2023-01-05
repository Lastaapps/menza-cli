from src import di
from . import util
from src.repo.repo import Repo
from result import Ok, Err
from src.api.agata_entity import Subsystem

def print_dish_list(repo: Repo, subsystem: Subsystem) -> None:
    res = repo.get_dish_list(subsystem)
    match res:
        case Ok(value):
            for (_, dishList) in value.items():
                for dish in dishList:
                    print(
                        dish.weight,
                        dish.name,
                        dish.price_student,
                        dish.price_normal,
                        ",".join(dish.allergens),
                        sep = '\t'
                    )
        case Err(e):
            print(e)

def command_dish(mocked: bool, phrase: str) -> None:
    repo = di.get_repo(mocked)
    menza = util.find_menza(repo, phrase)

    match menza:
        case Ok(value):
            print("Menu for " + value.description)
            print_dish_list(repo, value)
        case Err(e):
            print(e)
