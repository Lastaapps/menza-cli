"""Loads app config from the menza.conf file"""

import configparser as cp
from typing import Any

from result import Err, Ok, Result, as_result

CONFIG_FILE = "~/.config/menza.conf"

"""
Please don't steal these keys!

You can easily obtain you own by contacting
SUZ IT department for an Agata key
or me for a Lasta key.
Thank you for making the world a better place!
"""
DEFAULT_AGATA_URL_BASE = "https://agata.suz.cvut.cz"
DEFAULT_AGATA_URL_API = "/jidelnicky/JAPIV2/json_API.php"
DEFAULT_AGATA_KEY = "v1XiWjvD"
DEFAULT_LASTA_URL = "https://lastaapps.sh.cvut.cz/menza"
DEFAULT_LASTA_KEY = "menza-cli_15becd42-cbae-48b2-aa69-650d06763454"

# pylint: disable=R0913
# It is ok for data classes


class AppConfig:
    """Holds app config"""

    def __init__(
        self,
        agata_url_base: str,
        agata_url_api: str,
        agata_api_key: str,
        lasta_url: str,
        lasta_api_key: str,
        allergens: list[str],
    ):
        self.agata_url_base = agata_url_base
        self.agata_url_api = agata_url_api
        self.agata_api_key = agata_api_key
        self.lasta_url = lasta_url
        self.lasta_api_key = lasta_api_key
        self.allergens = allergens

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    def __eq__(self, obj: Any):
        return isinstance(obj, AppConfig) and obj.__dict__ == self.__dict__


class ConfigLoader:
    """Loads and parses config"""

    def __init__(self, file: str = CONFIG_FILE):
        self.file = file

    @staticmethod
    @as_result(Exception)
    def __parse_allergens(allergens: str) -> list[str]:
        """Parses allergens list from config"""

        if len(allergens) == 0:
            return []
        return list(
            map(
                lambda x: str(int(x)),
                allergens.split(","),
            )
        )

    @staticmethod
    def default() -> AppConfig:
        """Creates a default AppConfig"""

        return AppConfig(
            DEFAULT_AGATA_URL_BASE,
            DEFAULT_AGATA_URL_API,
            DEFAULT_AGATA_KEY,
            DEFAULT_LASTA_URL,
            DEFAULT_LASTA_KEY,
            [],
        )

    def load_config(self) -> Result[AppConfig, str]:
        """
        Parses configs
        Returns Err on parsing error, uses defaults if configs are missing
        """

        parser = cp.ConfigParser()
        try:
            parser.read(self.file)
        except cp.Error as error:
            return Err(str(error))

        menza = parser["DEFAULT"]

        agata_url_base = menza.get("agata_url_base", DEFAULT_AGATA_URL_BASE)
        agata_url_api = menza.get("agata_url_api", DEFAULT_AGATA_URL_API)
        agata_api_key = menza.get("agata_api_key", DEFAULT_AGATA_KEY)
        lasta_api_url = menza.get("lasta_url", DEFAULT_LASTA_URL)
        lasta_api_key = menza.get("lasta_api_key", DEFAULT_LASTA_KEY)

        allergens = ConfigLoader.__parse_allergens(menza.get("allergens", ""))
        match allergens:
            case Ok(value):
                allergens = value
            case Err(error):
                return Err(str(error))

        return Ok(
            AppConfig(
                agata_url_base,
                agata_url_api,
                agata_api_key,
                lasta_api_url,
                lasta_api_key,
                allergens,
            )
        )
