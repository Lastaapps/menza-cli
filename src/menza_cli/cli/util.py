"""Common utils for cli commands"""

from result import Err, Ok, Result

from menza_cli.api.agata_entity import Subsystem
from menza_cli.repo.repo import Repo


def find_menza(repo: Repo, phrase: str) -> Result[Subsystem, Exception]:
    """
    Finds a subsystem by it's id (int) or name (the first partial match).
    Returns Err otherwise or on a network error
    """

    data = repo.get_menza_list()
    match data:
        case Ok(value):
            if len(phrase) == 0:
                return Err(RuntimeError("Cannot search for no named menza."))

            if phrase.isnumeric():
                system_id = int(phrase)
                for menza in value:
                    if menza.id == system_id:
                        return Ok(menza)
                return Err(RuntimeError(f"No menza found with the id of {system_id}."))

            for menza in value:
                if phrase.lower() in menza.description.lower():
                    return Ok(menza)
            return Err(RuntimeError(f"No menza found with name of {phrase}"))

        case Err(_):
            return data
