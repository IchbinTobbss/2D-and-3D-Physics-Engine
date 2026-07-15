@echo off

echo Entferne Python-Pakete...

python -m pip uninstall arcade pymunk -y

echo Entferne Python...

winget uninstall Python.Python.3.13

echo.
echo Deinstallation fertig!

echo Loesche dieses Skript...
del "%~f0"