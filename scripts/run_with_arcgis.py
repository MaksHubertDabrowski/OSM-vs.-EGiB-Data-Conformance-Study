import subprocess
import sys
import os
from pathlib import Path

# Ścieżka do Pythona ArcGIS Pro
ARCGIS_PYTHON = r"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"

# Katalog Pixi (gdzie są nasze paczki)
PIXI_ENV = Path(__file__).parent.parent / ".pixi" / "envs" / "default"

# Dodaj site-packages z Pixi do PYTHONPATH
pixi_site_packages = PIXI_ENV / "Lib" / "site-packages"

env = os.environ.copy()
if pixi_site_packages.exists():
    current_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{pixi_site_packages};{current_pythonpath}"

# Uruchom skrypt używając Pythona z ArcGIS Pro
if len(sys.argv) < 2:
    print("Użycie: python run_with_arcgis.py <script.py>")
    sys.exit(1)

script_to_run = sys.argv[1]
result = subprocess.run(
    [ARCGIS_PYTHON, script_to_run],
    env=env,
    cwd=Path(__file__).parent.parent
)

sys.exit(result.returncode)