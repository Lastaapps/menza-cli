#!/bin/bash

VENV=".venv"

python3 -m venv "$VENV"
source "$VENV/bin/activate"
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "Don't forget to activate the virtual environment"
echo "source $VENV/bin/activate"
echo "Then you can run the app by running ./menza.py"

