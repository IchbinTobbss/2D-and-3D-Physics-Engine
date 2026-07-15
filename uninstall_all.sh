#!/bin/bash

ORDNER="$(cd "$(dirname "$0")" && pwd)"

echo "macOS erkannt."
echo "Ordner:"
echo "$ORDNER"

echo "Loesche alle Dateien ausser diesem Skript..."

find "$ORDNER" -mindepth 1 ! -name "$(basename "$0")" -exec rm -rf {} +

echo "Fertig!"