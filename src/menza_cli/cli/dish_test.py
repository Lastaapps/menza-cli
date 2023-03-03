"""Test dish command"""

from pytest import CaptureFixture

from .dish import command_dish

# pylint: disable=C0301
ANSWER = "Kocourkov\n200g\tUtopenec\t42.0\t69.0\t1,2,3\n\tUtopenka\t42.0\t69.0\t1,2,4\n"


def test_fixures(capsys: CaptureFixture):
    """Tests pytest"""

    print("Python je naprosté zlo")
    out = capsys.readouterr().out
    assert out == "Python je naprosté zlo\n"


def test_dish_empty(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_dish(True, "")
    out = capsys.readouterr().out
    assert out == "Cannot search for no named menza.\n"


def test_dish_id(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_dish(True, "1")
    out = capsys.readouterr().out
    assert out == ANSWER


def test_dish_complete(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_dish(True, "Kocourkov")
    out = capsys.readouterr().out
    assert out == ANSWER


def test_dish_partial(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_dish(True, "oco")
    out = capsys.readouterr().out
    assert out == ANSWER


def test_dish_unknown_id(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_dish(True, "42")
    out = capsys.readouterr().out
    assert out == "No menza found with the id of 42.\n"


def test_dish_unknown_name(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_dish(True, "befelemepeseveze")
    out = capsys.readouterr().out
    assert out == "No menza found with name of befelemepeseveze\n"
