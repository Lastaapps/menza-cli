"""Agata api impl tests"""

from menza_cli import di

from .agata_api import AgataApi


def get_api() -> AgataApi:
    """Creates an Api object with default configs"""

    return di.get_agata_api(False)


def test_get_sub_systems():
    """One of many tests"""

    api = get_api()
    res = api.get_sub_systems()
    assert len(res) == 12


def test_serving_places():
    """One of many tests"""

    api = get_api()
    res = api.get_serving_places(1)
    assert len(res) == 2


def test_dish_types():
    """One of many tests"""

    api = get_api()
    res = api.get_dish_types(1)
    assert len(res) == 8


def test_get_dishes():
    """One of many tests"""

    api = get_api()
    res = api.get_dishes(1)
    assert len(res) != 0


def test_info():
    """One of many tests"""

    api = get_api()
    res = api.get_info(1)
    assert len(res) == 1


def test_news():
    """One of many tests"""

    api = get_api()
    assert isinstance(api.get_news(1).header, str)


def test_get_open_times():
    """One of many tests"""

    api = get_api()
    res = api.get_open_times(1)
    assert len(res) == 6


def test_contact():
    """One of many tests"""

    api = get_api()
    res = api.get_contact()
    assert len(res) == 14


def test_week_info():
    """One of many tests"""

    api = get_api()
    res = api.get_week_info(1)
    assert len(res) != 0


def test_day_dish():
    """One of many tests"""

    api = get_api()
    res = api.get_week_info(1)
    res = api.get_day_dish(res[0].id)
    assert len(res) != 0


def test_image_url():
    """One of many tests"""

    api = get_api()
    res = api.get_image_url(1, "ahojky")
    assert (
        res
        == "https://agata.suz.cvut.cz/jidelnicky/showfoto.php?clPodsystem=1&xFile=ahojky"
    )
