"""Tests lasta api"""

from menza_cli import di

from .lasta_api import LastaApi


def get_api() -> LastaApi:
    """Creates an Api object with default configs"""

    return di.get_lasta_api(False)


def test_post_rating():
    """Tests a lasta api methods"""

    api = get_api()
    menza_id = "cli_test"
    dish_id = "monty_py"
    dish_name = "Štěkanátky"

    status1 = api.get_status(menza_id)
    statis1 = api.get_statistics()

    status2 = api.post_rating(menza_id, dish_id, dish_name, 3)
    statis2 = api.get_statistics()

    status3 = api.get_status(menza_id)
    statis3 = api.get_statistics()

    print(status2)
    print(status3)

    assert status1 != status2
    assert status2 == status3
    assert statis1 != statis2
    assert statis2 != statis3
