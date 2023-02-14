#!/bin/bash

INSTALL_DIR="/usr/share/menza-cli"
BRANCH="main"

# Exit on error
set -e

echo Checking root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [[ ! -d "${INSTALL_DIR}" ]]; then
  echo Creating dir
  mkdir -p "${INSTALL_DIR}"
fi

cd "${INSTALL_DIR}"
echo "Working in $(pwd)"

if [[ ! -d ./.git ]]; then
  echo Cloning
  git clone -b "${BRANCH}" -o origin https://github.com/Lastaapps/menza-cli.git .
  chmod +x *.sh
  chmod 755 run.sh

  ./setup.sh
else
  echo Pulling
  git fetch origin
  git checkout "${BRANCH}"
  git reset --hard origin/"${BRANCH}"
fi

if [[ ! -h /usr/bin/menza ]]; then
  echo Creating symlinks
  ln -s "${INSTALL_DIR}/run.sh" /usr/bin/menza
  ln -s "${INSTALL_DIR}/install.sh" /usr/bin/menza-update
  ln -s "${INSTALL_DIR}/uninstall.sh" /usr/bin/menza-uninstall
fi

printf "Done\n\n\n"

cat README.md

exit 0

