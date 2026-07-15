#!/bin/bash

echo "Entferne Python-Pakete..."

python3 -m pip uninstall arcade pymunk -y

echo "Entferne Python..."

brew uninstall python

echo
echo "Deinstallation fertig!"

echo "Loesche dieses Skript..."

rm -- "$0"