@echo off
echo Installiere Python...

winget install Python.Python.3.13 --accept-source-agreements --accept-package-agreements

echo.
echo Python Installation abgeschlossen.
echo Teste Python...

python --version

pause