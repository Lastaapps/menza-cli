"""Basic app dependency injection respecting configs and app mocking"""

from menza_cli.api.agata_api import AgataApi
from menza_cli.api.agata_api_impl import AgataApiImpl
from menza_cli.api.agata_api_mock import AgataApiMock
from menza_cli.api.lasta_api import LastaApi
from menza_cli.api.lasta_api_impl import LastaApiImpl
from menza_cli.api.lasta_api_mock import LastaApiMock
from menza_cli.config import AppConfig, ConfigLoader
from menza_cli.gui.main import Main
from menza_cli.repo.repo import Repo
from menza_cli.repo.repo_impl import RepoImpl

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


# Store default config (for tests)
store_config(ConfigLoader.default())


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
