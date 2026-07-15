#!/bin/bash

if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew ist nicht installiert."
    exit 1
fi

brew install python

python3 -m pip install --upgrade pip
python3 -m pip install arcade pymunk

echo "Installation abgeschlossen!"