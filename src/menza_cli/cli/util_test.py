"""Tests commands utils"""

from result import Err, Ok

from menza_cli import di
from menza_cli.repo.repo import Repo

from . import util


def get_repo() -> Repo:
    """Obtains a mocked repo instance"""
    return di.get_repo(True)


def test_find_menza_id():
    """Find menza test"""

    repo = get_repo()
    res = util.find_menza(repo, "1")
    assert isinstance(res, Ok)
    assert res.value.description == "Kocourkov"


def test_find_menza_partial():
    """Find menza test"""

    repo = get_repo()
    res = util.find_menza(repo, "oco")
    assert isinstance(res, Ok)
    assert res.value.description == "Kocourkov"


def test_find_menza_case():
    """Find menza test"""

    repo = get_repo()
    res = util.find_menza(repo, "kOCOURKOV")
    assert isinstance(res, Ok)
    assert res.value.description == "Kocourkov"


def test_find_menza_match():
    """Find menza test"""

    repo = get_repo()
    res = util.find_menza(repo, "Kocourkov")
    assert isinstance(res, Ok)
    assert res.value.description == "Kocourkov"


def test_find_menza_empty():
    """Find menza test"""

    repo = get_repo()
    res = util.find_menza(repo, "")
    assert isinstance(res, Err)
    assert str(res.value) == "Cannot search for no named menza."


def test_find_menza_invalid_id():
    """Find menza test"""

    repo = get_repo()
    res = util.find_menza(repo, "42")
    assert isinstance(res, Err)
    assert str(res.value) == "No menza found with the id of 42."


def test_find_menza_invalid_name():
    """Find menza test"""

    repo = get_repo()
    res = util.find_menza(repo, "bflmpsvz")
    assert isinstance(res, Err)
    assert str(res.value) == "No menza found with name of bflmpsvz"


def test_find_menza_negative_id():
    """Find menza test"""

    repo = get_repo()
    res = util.find_menza(repo, "-1")
    assert isinstance(res, Err)
    assert str(res.value) == "No menza found with name of -1"
