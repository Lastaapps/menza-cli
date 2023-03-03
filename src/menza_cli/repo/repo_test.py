"""Tests for repo"""

from result import Ok

from menza_cli import di
from menza_cli.api.agata_api import Subsystem
from menza_cli.api.agata_entity import Dish
from menza_cli.config import AppConfig, ConfigLoader

from .repo import DishRatingMapper, Repo

config: AppConfig = ConfigLoader.default()
config.allergens = ["1"]
di.store_config(config)

# pylint: disable=C0301

# Pylint ignores decorators and abstraction again
# pylint: disable=E1101

KOCOURKOV = Subsystem(
    {
        "id": 1,
        "popis": "Kocourkov",
        "otevreno": True,
        "jidelnicek_denni": True,
        "jidelnicek_tydenni": True,
        "poradi": 1,
    }
)


def get_repo() -> Repo:
    """Creates a repo instance for testing"""
    return di.get_repo(True)


def get_dish(repo: Repo = get_repo()) -> Dish:
    """Gets the first found dish"""

    dish_dict: dict[str, list[Dish]] = repo.get_dish_list(KOCOURKOV).value
    key = list(dish_dict.keys())
    return dish_dict[key[0]][0]


def test_get_menza_list():
    """Tests menza list"""

    repo = get_repo()
    res = repo.get_menza_list()
    assert isinstance(res, Ok)
    assert (
        str(res.value)
        == "[{'id': 1, 'description': 'Kocourkov', 'open': True, 'daily': True, 'weekly': True, 'order': 1}, {'id': 2, 'description': 'Bavorov', 'open': False, 'daily': True, 'weekly': True, 'order': 2}]"
    )


def test_get_dish_list():
    """Tests dish list"""

    repo = get_repo()
    res = repo.get_dish_list(KOCOURKOV)
    assert isinstance(res, Ok)
    print(res.value)
    assert (
        str(res.value)
        == "{'Polévka': [{'id': 1, 'subsystem_id': 1, 'date': '2022-12-24', 'serving_places': [1], 'type': 1, 'weight': '200g', 'name': 'Utopenec', 'side_dish_a': ' okurky', 'side_dish_b': ' lidi', 'price_student': 42.0, 'price_normal': 69.0, 'allergens': [1, 2, 3], 'photo': 'IMG-2022-12-12-142136203.JPG', 'active': True, 'complete': 'Utopenec okurky  lidi ', 'warn': False}], 'Specialita': [{'id': 2, 'subsystem_id': 1, 'date': '2022-12-24', 'serving_places': [1], 'type': 2, 'weight': '', 'name': 'Utopenka', 'side_dish_a': ' paprika', 'side_dish_b': ' člověci', 'price_student': 42.0, 'price_normal': 69.0, 'allergens': [1, 2, 4], 'photo': '', 'active': True, 'complete': 'Utopenka paprika  člověci ', 'warn': False}]}"
    )


def test_get_week_menu():
    """Tests menu"""

    repo = get_repo()
    res = repo.get_week_menu(KOCOURKOV)
    assert isinstance(res, Ok)
    assert (
        str(res.value)
        == "{'2022-12-23': [{'id': 1, 'id_week': 1, 'date': '2022-12-23', 'day_of_week': 4, 'type': 1, 'name': 'Žrádlo 1', 'weight': '69 g', 'type_name': 'Polejvka', 'day_of_week_name': 'Fri'}, {'id': 2, 'id_week': 1, 'date': '2022-12-23', 'day_of_week': 4, 'type': 2, 'name': 'Žrádlo 2', 'weight': '', 'type_name': 'Nakládka', 'day_of_week_name': 'Fri'}], '2022-12-24': [{'id': 3, 'id_week': 1, 'date': '2022-12-24', 'day_of_week': 5, 'type': 3, 'name': 'Žrádlo 3', 'weight': '42 ks', 'type_name': 'Dokrmka', 'day_of_week_name': 'Sat'}, {'id': 4, 'id_week': 1, 'date': '2022-12-24', 'day_of_week': 5, 'type': 4, 'name': 'Žrádlo 4', 'weight': '420 ml', 'type_name': 'Dezertér', 'day_of_week_name': 'Sat'}]}"
    )


def test_get_complete_info():
    """Tests complete info"""

    repo = get_repo()
    res = repo.get_complete_info(KOCOURKOV)
    assert isinstance(res, Ok)
    assert (
        str(res.value)
        == "{'header': 'Horni', 'footer': 'Dolni', 'times': {1: [{'id': 108, 'subsytem_id': 1, 'serving_id': 1, 'serving_name': 'Restaurace', 'serving_abbrev': 'R', 'serving_order': 1, 'from_desc': '', 'from_order': '1', 'day_from': 'Po', 'day_to': 'Čt', 'time_from': '11:00', 'time_to': '20:00'}, {'id': 101, 'subsytem_id': 1, 'serving_id': 1, 'serving_name': 'Restaurace', 'serving_abbrev': 'R', 'serving_order': 1, 'from_desc': '', 'from_order': '2', 'day_from': 'Pá', 'day_to': '', 'time_from': '11:00', 'time_to': '19:30'}], 2: [{'id': 13, 'subsytem_id': 1, 'serving_id': 2, 'serving_name': 'Jídelna', 'serving_abbrev': 'J', 'serving_order': 2, 'from_desc': 'Snídaně', 'from_order': '1', 'day_from': 'Po', 'day_to': 'Pá', 'time_from': '6:30', 'time_to': '9:30'}, {'id': 97, 'subsytem_id': 1, 'serving_id': 2, 'serving_name': 'Jídelna', 'serving_abbrev': 'J', 'serving_order': 2, 'from_desc': 'Oběd', 'from_order': '2', 'day_from': 'Po', 'day_to': 'Pá', 'time_from': '11:00', 'time_to': '14:30'}, {'id': 105, 'subsytem_id': 1, 'serving_id': 2, 'serving_name': 'Jídelna', 'serving_abbrev': 'J', 'serving_order': 2, 'from_desc': 'Večeře', 'from_order': '3', 'day_from': 'Po', 'day_to': 'Čt', 'time_from': '17:00', 'time_to': '20:00'}, {'id': 109, 'subsytem_id': 1, 'serving_id': 2, 'serving_name': 'Jídelna', 'serving_abbrev': 'J', 'serving_order': 2, 'from_desc': 'Večeře', 'from_order': '4', 'day_from': 'Pá', 'day_to': 'Pá', 'time_from': '17:00', 'time_to': '19:30'}]}, 'contacts': [{'id': 1, 'subsystem_id': 1, 'gps': '50.079174,14.393236', 'order': 1, 'role': 'Vedoucí menzy', 'name': '', 'phone': '234678291', 'email': 'menza-strahov@cvut.cz'}, {'id': 2, 'subsystem_id': 1, 'gps': '50.079174,14.393236', 'order': 2, 'role': 'Provoz', 'name': '', 'phone': '234678361', 'email': 'suz-provoznims@cvut.cz'}], 'addresses': [{'id': 1, 'subsystem_id': 1, 'subsystem_name': 'Kocourkov', 'address': 'Kocourkov 42', 'gps': '50N 15E'}]}"
    )


def test_get_image_url():
    """Tests image url"""

    repo = get_repo()
    dish = get_dish(repo)
    res = repo.get_image_url(dish)
    assert (
        res
        == "https://agata.suz.cvut.cz/jidelnicky/showfoto.php?clPodsystem=1&xFile=IMG-2022-12-12-142136203.JPG"
    )


def test_get_rating():
    """Tests rating"""

    repo = get_repo()
    dish = get_dish(repo)

    res: Ok[DishRatingMapper] = repo.get_rating()
    assert isinstance(res, Ok)
    mapper: DishRatingMapper = res.value

    state1 = mapper(KOCOURKOV, dish)
    rating_res = repo.send_rating(KOCOURKOV, dish, 3)
    state2 = mapper(KOCOURKOV, dish)

    assert isinstance(rating_res, Ok)
    assert state1 != state2
