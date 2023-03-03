"""Test week command"""

from pytest import CaptureFixture

from .week import command_week

# pylint: disable=C0301
ANSWER = "Kocourkov\n\n2022-12-23 Fri\nPolejvka\t69 g\tŽrádlo 1\nNakládka\t\tŽrádlo 2\n\n2022-12-24 Sat\nDokrmka\t42 ks\tŽrádlo 3\nDezertér\t420 ml\tŽrádlo 4\n"


def test_fixures(capsys: CaptureFixture):
    """Tests pytest"""

    print("Python je naprosté zlo")
    out = capsys.readouterr().out
    assert out == "Python je naprosté zlo\n"


def test_week_empty(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_week(True, "")
    out = capsys.readouterr().out
    assert out == "Cannot search for no named menza.\n"


def test_week_id(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_week(True, "1")
    out = capsys.readouterr().out
    assert out == ANSWER


def test_week_complete(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_week(True, "Kocourkov")
    out = capsys.readouterr().out
    assert out == ANSWER


def test_week_partial(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_week(True, "oco")
    out = capsys.readouterr().out
    assert out == ANSWER


def test_week_unknown_id(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_week(True, "42")
    out = capsys.readouterr().out
    assert out == "No menza found with the id of 42.\n"


def test_week_unknown_name(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_week(True, "befelemepeseveze")
    out = capsys.readouterr().out
    assert out == "No menza found with name of befelemepeseveze\n"
