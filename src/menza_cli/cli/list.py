"""Handles list cli command"""

from result import Err, Ok

from menza_cli import di


def command_list(mocked: bool):
    """Handles list cli command"""

    repo = di.get_repo(mocked)
    menzas = repo.get_menza_list()
    match menzas:
        case Ok(value):
            for menza in value:
                opened = "O" if menza.open else "X"
                print(f"{menza.id :2d}", opened, menza.description, sep="\t")
        case Err(error):
            print(error)
