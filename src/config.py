"""Loads app config from the menza.conf file"""

import configparser as cp

from result import Err, Ok, Result, as_result

CONFIG_FILE = "menza.conf"

# pylint: disable=R0913
# It is ok for data classes

class AppConfig:
    """Holds app config"""

    def __init__(
        self,
        agata_api_key: str,
        agata_url_base: str,
        agata_url_api: str,
        lasta_api_key: str,
        lasta_url: str,
        allergens: list[str],
    ):
        self.agata_api_key = agata_api_key
        self.agata_url_base = agata_url_base
        self.agata_url_api = agata_url_api
        self.lasta_api_key = lasta_api_key
        self.lasta_url = lasta_url
        self.allergens = allergens


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

        agata_api_key = menza.get("agata_api_key", "v1XiWjvD")
        agata_url_base = menza.get("agata_url_base", "https://agata.suz.cvut.cz")
        agata_url_api = menza.get("agata_url_api", "/jidelnicky/JAPI/json_API.php")
        lasta_api_key = menza.get(
            "lasta_api_key", "menza-cli_15becd42-cbae-48b2-aa69-650d06763454"
        )
        lasta_api_url = menza.get("lasta_url", "https://lastaapps.sh.cvut.cz/menza")

        allergens = ConfigLoader.__parse_allergens(menza.get("allergens", ""))
        match allergens:
            case Ok(value):
                allergens = value
            case Err(error):
                return Err(str(error))

        return Ok(
            AppConfig(
                agata_api_key,
                agata_url_base,
                agata_url_api,
                lasta_api_key,
                lasta_api_url,
                allergens,
            )
        )
