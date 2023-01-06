"""Test list command"""

from pytest import CaptureFixture

from src import di
from src.config import AppConfig, ConfigLoader

from .list import command_list

config: AppConfig = ConfigLoader().load_config(default=True).value
di.store_config(config)


def test_list_empty(capsys: CaptureFixture):
    """Tests an input for the command"""

    command_list(True)
    out = capsys.readouterr().out
    assert out == " 1\tO\tKocourkov\n 2\tX\tBavorov\n"
