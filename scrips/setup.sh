#!/bin/bash

VENV=".venv"

PYT3_VERSION="$(python3 --version | cut -d ' ' -f2 | cut -d '.' -f2)"
PYT3_MIN="10" # Python 3.10 required

if [ $PYT3_MIN -gt $PYT3_VERSION ]; then
    echo "Your python version 3.$PYT3_VERSION is not supported"
    echo "Use at least python 3.$PYT3_MIN"
    exit
fi

echo "Seting up venv in $VENV"
echo Using Python $(python3 --version)

python3 -m venv "$VENV"
source "$VENV/bin/activate"

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "Don't forget to activate the virtual environment"
echo "source $VENV/bin/activate"
echo "Then you can run the app by running ./menza.py"


# if which xdg-open &> /dev/null; then
#     true
# else
#     echo "xdgs-open is not installed, you can't view images!"
# fi

exit
