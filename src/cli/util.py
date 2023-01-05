from src.repo.repo import Repo
from result import Result, Ok, Err
from src.api.agata_entity import Subsystem


def find_menza(repo: Repo, phrase: str) -> Result[Subsystem, Exception]:
    data = repo.get_menza_list()
    match data:
        case Ok(value):
            if len(phrase) == 0:
                return Err(RuntimeError(f"Cannot search for no named menza."))

            if phrase.isnumeric():
                id = int(phrase)
                for menza in value:
                    if menza.id == id:
                        return Ok(menza)
                return Err(RuntimeError(f"No menza found with the id of {id}."))

            for menza in value:
                if phrase.lower() in menza.description.lower():
                    return Ok(menza)
            return Err(RuntimeError(f"No menza found with name of {phrase}"))

        case Err(_):
            return data
