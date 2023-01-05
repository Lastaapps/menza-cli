from src.repo.repo import Repo
from src.repo.repo_impl import RepoImpl
from src.api.agata_api import AgataApi
from src.api.agata_api_impl import AgataApiImpl
from src.api.agata_api_mock import AgataApiMock
from src.api.lasta_api import LastaApi
from src.api.lasta_api_impl import LastaApiImpl
from src.api.lasta_api_mock import LastaApiMock
from src.gui.main import Main

from src.config import AppConfig

__config: AppConfig


def store_config(config: AppConfig) -> None:
    global __config
    __config = config


def get_config() -> AppConfig:
    return __config


def get_agata_api(mocked: bool) -> AgataApi:
    if not mocked:
        config = get_config()
        return AgataApiImpl(
            config.agata_url_base,
            config.agata_url_api,
            config.agata_api_key,
        )
    else:
        return AgataApiMock()


def get_lasta_api(mocked: bool) -> LastaApi:
    if not mocked:
        config = get_config()
        return LastaApiImpl(config.lasta_url, config.lasta_api_key)
    else:
        return LastaApiMock()


def get_repo(mocked: bool) -> Repo:
    config = get_config()
    return RepoImpl(
        get_agata_api(mocked),
        get_lasta_api(mocked),
        config.allergens,
    )


def get_main_gui(mocked: bool) -> Main:
    return Main(get_repo(mocked))
