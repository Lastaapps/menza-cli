#!/bin/bash

INSTALL_DIR="/usr/share/menza-cli"

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

unlink /usr/bin/menza
unlink /usr/bin/menza-update
unlink /usr/bin/menza-uninstall

rm -rf "${INSTALL_DIR}"

echo Done
exit 0
