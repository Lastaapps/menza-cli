"""Test list command"""

from pytest import CaptureFixture

from .list import command_list


def test_list_empty(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_list(True)
    out = capsys.readouterr().out
    assert out == " 1\tO\tKocourkov\n 2\tX\tBavorov\n"
