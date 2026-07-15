import os
import subprocess

url = "https://github.com/IchbinTobbss/Tobbss-Framework"

if not os.path.exists("framework"):
    subprocess.run(["git", "clone", url, "framework"], check=True)
datei = os.path.abspath(__file__)
os.remove(datei)