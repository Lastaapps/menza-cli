from result import Err, Ok

from src import di


def command_list(mocked: bool):
    repo = di.get_repo(mocked)
    menzas = repo.get_menza_list()
    match menzas:
        case Ok(value):
            for menza in value:
                open = "O" if menza.open else "X"
                print(f"{menza.id :2d}", open, menza.description, sep="\t")
        case Err(e):
            print(e)
