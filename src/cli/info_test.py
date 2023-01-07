"""Test info command"""

from pytest import CaptureFixture

from .info import command_info

# pylint: disable=C0301
ANSWER = "Kocourkov\nHorni \n\nDolni \n\nRestaurace\nPo - Čt  11:00 - 20:00  \nPá       11:00 - 19:30  \n\nJídelna\nPo - Pá   6:30 -  9:30  Snídaně\nPo - Pá  11:00 - 14:30  Oběd\nPo - Čt  17:00 - 20:00  Večeře\nPá       17:00 - 19:30  Večeře\n\nVedoucí menzy\nmenza-strahov@cvut.cz\n+420 234 678 291\n\nProvoz\nsuz-provoznims@cvut.cz\n+420 234 678 361\n\nKocourkov 42\n50N 15E\n"


def test_fixures(capsys: CaptureFixture):
    """Tests pytest"""

    print("Python je naprosté zlo")
    out = capsys.readouterr().out
    assert out == "Python je naprosté zlo\n"


def test_info_empty(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_info(True, "")
    out = capsys.readouterr().out
    assert out == "Cannot search for no named menza.\n"


def test_info_id(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_info(True, "1")
    out = capsys.readouterr().out
    assert out == ANSWER


def test_info_complete(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_info(True, "Kocourkov")
    out = capsys.readouterr().out
    assert out == ANSWER


def test_info_partial(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_info(True, "oco")
    out = capsys.readouterr().out
    assert out == ANSWER


def test_info_unknown_id(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_info(True, "42")
    out = capsys.readouterr().out
    assert out == "No menza found with the id of 42.\n"


def test_info_unknown_name(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_info(True, "befelemepeseveze")
    out = capsys.readouterr().out
    assert out == "No menza found with name of befelemepeseveze\n"
