"""Tests for app config file"""

from result import Err, Ok

from menza_cli.config import AppConfig, ConfigLoader


def test_default():
    """Test a config given"""

    loader = ConfigLoader("res/test/config_default.conf")
    config = loader.load_config()
    expected = ConfigLoader.default()
    assert isinstance(config, Ok)
    assert config.value == expected


def test_empty():
    """Test a config given"""

    loader = ConfigLoader("res/test/config_empty.conf")
    config = loader.load_config()
    expected = ConfigLoader.default()
    assert isinstance(config, Ok)
    assert config.value == expected


def test_non_existing():
    """Test a config given"""

    loader = ConfigLoader("res/test/config_non_existing.conf")
    config = loader.load_config()
    expected = ConfigLoader.default()
    assert isinstance(config, Ok)
    assert config.value == expected


def test_full():
    """Test a config given"""

    loader = ConfigLoader("res/test/config_full.conf")
    config = loader.load_config()
    expected = AppConfig(
        "agata_url_base_config",
        "agata_url_api_config",
        "agata_api_key_config",
        "lasta_url_config",
        "lasta_api_key_config",
        ["1", "3"],
    )
    assert isinstance(config, Ok)
    assert config.value == expected


def test_unknown():
    """Test a config given"""

    loader = ConfigLoader("res/test/config_unknown.conf")
    config = loader.load_config()
    expected = ConfigLoader.default()
    assert isinstance(config, Ok)
    assert config.value == expected


def test_malformed_allergens():
    """Test a config given"""

    loader = ConfigLoader("res/test/config_malformed_allergens.conf")
    config = loader.load_config()
    assert isinstance(config, Err)


def test_no_default():
    """Test a config given"""

    loader = ConfigLoader("res/test/config_no_default.conf")
    config = loader.load_config()
    assert isinstance(config, Err)
