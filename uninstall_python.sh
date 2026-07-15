#!/bin/bash

echo "Entferne Python..."

brew uninstall python

echo "Deinstallation fertig!"

echo "Loesche dieses Skript..."

rm -- "$0"