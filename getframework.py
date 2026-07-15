import os
import subprocess

url = "https://github.com/IchbinTobbss/Tobbss-Framework"

if not os.path.exists("Tobbss-Framework"):
    subprocess.run(["git", "clone", url, "Tobbss-Framework"], check=True)
datei = os.path.abspath(__file__)
os.remove(datei)