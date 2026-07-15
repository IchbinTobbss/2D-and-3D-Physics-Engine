import urllib.request
import subprocess
import sys
import os

# Lokale Version
VERSION_FILE = "version.txt"

# GitHub Datei mit der aktuellen Version
VERSION_URL = "https://raw.githubusercontent.com/IchbinTobbss/Tobbss-Framework/main/version.txt"


def get_local_version():
    try:
        with open(VERSION_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "0.0.0"


def get_latest_version():
    try:
        with urllib.request.urlopen(VERSION_URL) as response:
            return response.read().decode("utf-8").strip()
    except Exception:
        return None


def start_installer():
    print("Update verfügbar!")
    
    # Später anpassen:
    # startet deinen TobiInstaller
    installer = "TobiInstaller.app"

    if os.path.exists(installer):
        subprocess.Popen(["open", installer])
    else:
        print("Installer nicht gefunden!")


def main():

    local = get_local_version()
    latest = get_latest_version()

    print(f"Installiert: {local}")
    print(f"Aktuell:     {latest}")


    if latest is None:
        print("Keine Internetverbindung oder GitHub nicht erreichbar.")
        return


    if local != latest:
        start_installer()
    else:
        print("Framework ist aktuell.")


if __name__ == "__main__":
    main()
