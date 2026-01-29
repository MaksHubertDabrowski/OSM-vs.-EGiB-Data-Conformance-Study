import os
from pathlib import Path
from loguru import logger

install_dir = r"C:\Program Files\ArcGIS\Pro"
conda_env_dir = os.path.join(install_dir, r"bin\Python\envs\arcgispro-py3")

paths_to_check = [
    install_dir,
    os.path.join(install_dir, "bin"),
    conda_env_dir,
    os.path.join(conda_env_dir, r"Library\bin"),
    os.path.join(install_dir, r"Resources\ArcPy"),
    os.path.join(conda_env_dir, r"Lib\site-packages"),
]

logger.info("🔍 Sprawdzam strukturę katalogów ArcGIS Pro:")
for p in paths_to_check:
    exists = "✅" if os.path.exists(p) else "❌"
    logger.info(f"{exists} {p}")
    
    # Jeśli istnieje katalog bin, pokaż kilka pierwszych plików
    if os.path.exists(p) and "bin" in p:
        try:
            files = list(Path(p).glob("*.dll"))[:5]
            if files:
                logger.info(f"   Przykładowe DLL: {[f.name for f in files]}")
        except:
            pass

# Sprawdź też gdzie jest _arcgisscripting.pyd
logger.info("\n🔍 Szukam _arcgisscripting.pyd:")
for root, dirs, files in os.walk(install_dir):
    for file in files:
        if file.startswith("_arcgisscripting") and file.endswith(".pyd"):
            full_path = os.path.join(root, file)
            logger.success(f"Znaleziono: {full_path}")