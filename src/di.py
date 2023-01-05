from src.repo.repo import Repo
from src.repo.repo_impl import RepoImpl
from src.api.agata_api import AgataApi
from src.api.agata_api_impl import AgataApiImpl
from src.api.agata_api_mock import AgataApiMock
from src.api.lasta_api import LastaApi
from src.api.lasta_api_impl import LastaApiImpl
from src.api.lasta_api_mock import LastaApiMock
from src.gui.main import Main

def get_agata_api(mocked: bool) -> AgataApi:
    if not mocked:
        return AgataApiImpl()
    else:
        return AgataApiMock()

def get_lasta_api(mocked: bool) -> LastaApi:
    if not mocked:
        return LastaApiImpl()
    else:
        return LastaApiMock()

def get_repo(mocked: bool) -> Repo:
    return RepoImpl(
        get_agata_api(mocked),
        get_lasta_api(mocked),
    )

def get_main_gui(mocked: bool) -> Main:
    return Main(get_repo(mocked))
