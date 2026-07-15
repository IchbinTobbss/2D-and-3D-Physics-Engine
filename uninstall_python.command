#!/bin/bash

python3 -m pip uninstall -y arcade pymunk

if command -v brew >/dev/null 2>&1; then
    brew uninstall python
fi

echo "Deinstallation abgeschlossen!"