#!/bin/bash

echo "Installiere Homebrew..."

if ! command -v brew >/dev/null 2>&1; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Homebrew für Apple Silicon (M1–M5) in dieser Sitzung aktivieren
    if [ -f /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    fi
else
    echo "Homebrew ist bereits installiert."
fi

echo "Homebrew-Version:"
brew --version