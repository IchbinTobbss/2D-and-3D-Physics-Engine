#!/bin/bash

echo "Installiere Python..."

# Prüfen ob Homebrew vorhanden ist
if ! command -v brew &> /dev/null
then
    echo "Homebrew fehlt. Installiere Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

echo "Installiere Python..."
brew install python

echo ""
echo "Python Version:"
python3 --version

echo "Fertig!"