"""Tests click args parsing"""

from click.testing import CliRunner

from menza_cli import di
from menza_cli.clickargs import app
from menza_cli.config import AppConfig, ConfigLoader

config: AppConfig = ConfigLoader.default()
config.allergens = ["1"]
di.store_config(config)

# pylint: disable=C0301


def test_mock():
    """Test --mock option"""

    runner1 = CliRunner()
    result1 = runner1.invoke(app, ["--mocked", "list"])
    assert result1.exit_code == 0
    runner2 = CliRunner()
    result2 = runner2.invoke(app, ["list"])
    assert result2.exit_code == 0
    assert result1.output != result2.output


def test_list():
    """Tests the list command"""

    runner = CliRunner()
    result = runner.invoke(app, ["--mocked", "list"])
    assert result.exit_code == 0
    assert result.output == " 1\tO\tKocourkov\n 2\tX\tBavorov\n"


def test_dish():
    """Tests the dish command"""

    runner = CliRunner()
    result = runner.invoke(app, ["--mocked", "dish", "Kocourkov"])
    assert result.exit_code == 0
    assert (
        result.output
        == "Kocourkov\n200g\tUtopenec\t42.0\t69.0\t1,2,3\n\tUtopenka\t42.0\t69.0\t1,2,4\n"
    )


def test_week():
    """Tests the week command"""

    runner = CliRunner()
    result = runner.invoke(app, ["--mocked", "week", "Kocourkov"])
    assert result.exit_code == 0
    assert (
        result.output
        == "Kocourkov\n\n2022-12-23 Fri\nPolejvka\t69 g\tŽrádlo 1\nNakládka\t\tŽrádlo 2\n\n2022-12-24 Sat\nDokrmka\t42 ks\tŽrádlo 3\nDezertér\t420 ml\tŽrádlo 4\n"
    )


def test_info():
    """Tests the info command"""

    runner = CliRunner()
    result = runner.invoke(app, ["--mocked", "info", "Kocourkov"])
    assert result.exit_code == 0
    assert (
        result.output
        == "Kocourkov\nHorni \n\nDolni \n\nRestaurace\nPo - Čt  11:00 - 20:00  \nPá       11:00 - 19:30  \n\nJídelna\nPo - Pá   6:30 -  9:30  Snídaně\nPo - Pá  11:00 - 14:30  Oběd\nPo - Čt  17:00 - 20:00  Večeře\nPá       17:00 - 19:30  Večeře\n\nVedoucí menzy\nmenza-strahov@cvut.cz\n+420 234 678 291\n\nProvoz\nsuz-provoznims@cvut.cz\n+420 234 678 361\n\nKocourkov 42\n50N 15E\n"
    )


def test_unknown_option():
    """Tests unknown option"""

    runner = CliRunner()
    result = runner.invoke(app, ["--sus"])
    assert result.exit_code != 0


def test_unknown_command():
    """Tests unknown option"""

    runner = CliRunner()
    result = runner.invoke(app, ["sus"])
    assert result.exit_code != 0
