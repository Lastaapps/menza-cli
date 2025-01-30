#!/usr/bin/env python3
# /bin/ is omitted because venv is expected
"""Menza main file"""

from result import Ok, Err
from .clickargs import app
from .config import ConfigLoader
from . import di
import logging


def main():
    """Starts the app, loads config and starts click"""

    # Init config
    loaded = ConfigLoader().load_config()

    match loaded:
        case Ok(value):
            if value.logging:
                logging.basicConfig(
                    filename="menza.log",
                    encoding="utf-8",
                    level=logging.DEBUG,
                )
            else:
                logging.disable()

            di.store_config(value)
        case Err(error):
            print(error)
            return

    logging.info("Starting")
    logging.debug("Debug logs enabled")

    app()


if __name__ == "__main__":
    main()
