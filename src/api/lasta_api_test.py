"""Tests lasta api"""

from src.config import AppConfig, ConfigLoader

from .lasta_api_impl import LastaApiImpl


def get_api() -> LastaApiImpl:
    """Creates an Api object with default configs"""

    config: AppConfig = ConfigLoader().load_config(default=True).value
    api = LastaApiImpl(config.lasta_url, config.lasta_api_key)
    return api


def test_id():
    """Tests a lasta api methods"""

    api = get_api()
    dish_id = api.dish_id("Strahov", "Hromničková")
    assert dish_id == "yyICfxlF"


def test_():
    """Tests a lasta api methods"""

    api = get_api()
    dish_id = "monty_py"

    status1 = api.get_status()
    statis1 = api.get_statistics()

    status2 = api.post_rating(dish_id, 3)
    statis2 = api.get_statistics()

    status3 = api.get_status()
    statis3 = api.get_statistics()

    print(status2)
    print(status3)

    assert status1 != status2
    assert status2 == status3
    assert statis1 != statis2
    assert statis2 != statis3
