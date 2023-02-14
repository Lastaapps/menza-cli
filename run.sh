#!/bin/bash

set -e

cd /usr/share/menza-cli

source ./.venv/bin/activate

python3 menza.py

exit 0
