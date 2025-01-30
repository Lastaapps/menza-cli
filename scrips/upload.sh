#!/usr/bin/env bash

set +e

echo "Upgrading"
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine

echo "Building"
python3 -m build

echo "Uploading"
echo "Username: __token__"
echo "Password: see your password manager"
python3 -m twine upload --verbose dist/*
# python3 -m twine upload --verbose --repository testpypi dist/*

echo "Done"

