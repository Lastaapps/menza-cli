#!python3
# /bin/ is omitted because venv is expected
"""Menza main file"""

from result import Ok, Err
from .clickargs import app
from .config import ConfigLoader
from . import di


def main():
    """Starts the app, loads config and starts click"""

    # Init config
    loaded = ConfigLoader().load_config()
    match loaded:
        case Ok(value):
            di.store_config(value)
        case Err(error):
            print(error)
            return

    # Start click
    app()


if __name__ == "__main__":
    main()

