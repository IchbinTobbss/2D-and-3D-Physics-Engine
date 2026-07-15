#!/bin/bash

echo "Entferne Python..."

# Falls Python mit Homebrew installiert wurde
if command -v brew &> /dev/null; then
    brew uninstall python 2>/dev/null
fi

# Entferne eine normale Python.org Installation
sudo rm -rf /Library/Frameworks/Python.framework/Versions/*

# Entferne Verknüpfungen (falls vorhanden)
sudo rm -f /usr/local/bin/python3
sudo rm -f /usr/local/bin/pip3

echo ""
echo "Python wurde entfernt."
echo "Bitte starte den Mac neu."