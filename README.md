# Menza CLI
[![PyPI version](https://badge.fury.io/py/menza_cli.svg)](https://badge.fury.io/py/menza_cli)

Menza CLI is a command line tool written in Python (what a mistake)
allowing not only CTU students to view CTU Canteens menus.
Today menu, week menu, canteens info and dish rating using own rating BE
interconnected with my Android app is supported.

Because the Gui of the project is written using the ncurses library,
**non-unix systems are not supported**.

Make sure your terminal supports emojis.

# Install

**Python 3.10+ required!** Check by running `python3 --version`.

You can install the app from [pypi](https://pypi.org/project/menza-cli/).

```bash
# install the package
python3 -m pip install menza_cli

# If you don't have python in your PATH
# Bash
printf '\nexport PATH="$PATH:$HOME/.local/bin"\n\n' >> ~/.bashrc
source ~/.bashrc
# zsh
printf '\nexport PATH="$PATH:$HOME/.local/bin"\n\n' >> ~/.zshrc
source ~/.zshrc

# Run the app
menza
```

# Setup locally
To set the project you will need Python 3.10 or greater.
You can just run the `./scripts/setup.sh` script or create a virtual environment yourself
from the `requirements.txt` file included.

# Running
To run the app, source the created env using `source .venv/bin/activate` and run `./menza.sh --help`

To use mocked data (eg. it is weekend and no dish is served), pass the `--mocked` option.

## Gui
To run the app in Gui mode, omit any command while executing from CLI. You can navigate like
a chad using basic Vim binding or like a VŠE student using arrows.

### Controls
- `right/left` - switch between menu and main view
- `up/down` - move in menus/lists
- `Enter/o` - in menu load selected canteen menu, in the menu view open dish photo in browser if available
- `w` - switch to week view and back
- `r` - rate selected dish
- `q/Esc` - quit

To be warned against allergens view the config section below.

If the images are being opend twice in a brower it is not my fault, Python the stupid one here.


## Cli
To just get basic overview of one specific system, you can use a command in the CLI - `list`, `dish`, `week` or `info`.

The first 3 output data in Tab separated format, so they can be used by CLI filters.

Last 3 expect a cafeteria id (run the `list` command) or name, at least partially - the first system that matches gets used.

So to view a menu in the Strahov cafeteria, you can run any of these:
- `./menza.py dish 1`
- `./menza.py dish Strahov`
- `./menza.py dish str`

## Config file
You can config some basic app behavior using `menza.conf` file in the `~/.config` directory. The file is not required to exist.
File format is as follow:

```conf
# Required
[DEFAULT]

# if something changes in the future and project is no longer maintained
agata_url_base=
agata_url_api=
agata_api_key=
lasta_url=
lasta_api_key=

# Dishes with the following allergens will be grayed out
allergens=1,3
```

# License
Menza CLI is licensed under the `GNU GPL v3.0` license.
