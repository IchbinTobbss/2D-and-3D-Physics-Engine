@echo off
echo Windows erkannt.
echo Ordner:
echo %~dp0

echo Loesche alle Dateien ausser diesem Skript...

for %%F in ("%~dp0*") do (
    if /I not "%%~nxF"=="install.cmd" del /q "%%F"
)

for /d %%D in ("%~dp0*") do (
    rmdir /s /q "%%D"
)

echo Fertig!
pause