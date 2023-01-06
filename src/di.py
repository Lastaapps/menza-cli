"""Basic app dependency injection respecting configs and app mocking"""

from src.api.agata_api import AgataApi
from src.api.agata_api_impl import AgataApiImpl
from src.api.agata_api_mock import AgataApiMock
from src.api.lasta_api import LastaApi
from src.api.lasta_api_impl import LastaApiImpl
from src.api.lasta_api_mock import LastaApiMock
from src.config import AppConfig
from src.gui.main import Main
from src.repo.repo import Repo
from src.repo.repo_impl import RepoImpl

# pylint: disable=C0103,W0603
# This global is valid and it is no a constant
__config: AppConfig


def store_config(config: AppConfig) -> None:
    """Stores configs singleton to the di"""
    global __config
    __config = config


def get_config() -> AppConfig:
    """Gets the configs singleton"""
    return __config


def get_agata_api(mocked: bool) -> AgataApi:
    """Creates an Agata api instance"""

    if mocked:
        return AgataApiMock()

    config = get_config()
    return AgataApiImpl(
        config.agata_url_base,
        config.agata_url_api,
        config.agata_api_key,
    )


def get_lasta_api(mocked: bool) -> LastaApi:
    """Creates a Lasta api instance"""

    if mocked:
        return LastaApiMock()

    config = get_config()
    return LastaApiImpl(config.lasta_url, config.lasta_api_key)


def get_repo(mocked: bool) -> Repo:
    """Creates a Repo instance"""

    config = get_config()
    return RepoImpl(
        get_agata_api(mocked),
        get_lasta_api(mocked),
        config.allergens,
    )


def get_main_gui(mocked: bool) -> Main:
    """Creates a Main gui instance"""

    return Main(get_repo(mocked))
