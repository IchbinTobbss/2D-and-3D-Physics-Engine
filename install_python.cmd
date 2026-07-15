@echo off

echo Installiere Python...

winget install Python.Python.3.13 --accept-source-agreements --accept-package-agreements

echo.
echo Installation fertig!

echo Loesche dieses Skript...
del "%~f0"