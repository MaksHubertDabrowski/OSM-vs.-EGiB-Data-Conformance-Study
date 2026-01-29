import sys
import os
from loguru import logger

def setup_arcgis_complete():
    """
    Kompletna konfiguracja (The "Nuclear" Method).
    Dodaje wszystkie możliwe ścieżki binarne ArcGIS Pro.
    """
    # Główny katalog instalacyjny
    install_dir = r"C:\Program Files\ArcGIS\Pro"
    conda_env_dir = os.path.join(install_dir, r"bin\Python\envs\arcgispro-py3")
    
    # --- LISTA WSZYSTKICH WYMAGANYCH KATALOGÓW DLL ---
    dll_paths = [
        # 1. Główny silnik ArcGIS (tutaj jest ArcGISPro.exe i główne DLL)
        os.path.join(install_dir, "bin"),
        
        # 2. Biblioteki Conda wewnątrz ArcGIS (TUTAJ BRAKOWAŁO!)
        # To tutaj leżą zależności systemowe ArcPy (openssl, itp.)
        os.path.join(conda_env_dir, r"Library\bin"),
    ]

    # --- KROK 1: Odblokowanie DLL (Python 3.8+) ---
    logger.info("🔓 Odblokowywanie bibliotek DLL...")
    for p in dll_paths:
        if os.path.exists(p):
            # Dodaj do PATH (dla starszych systemów/zależności)
            if p not in os.environ["PATH"]:
                os.environ["PATH"] = p + ";" + os.environ["PATH"]
            
            # Dodaj do bezpiecznej listy DLL Pythona
            try:
                if hasattr(os, 'add_dll_directory'):
                    os.add_dll_directory(p)
            except Exception as e:
                logger.warning(f"⚠️ Nie udało się dodać DLL directory: {p} ({e})")
        else:
            logger.error(f"❌ Nie znaleziono katalogu DLL: {p}")

    # --- KROK 2: Wskazanie bibliotek Python (site-packages) ---
    python_paths = [
        os.path.join(install_dir, r"Resources\ArcPy"),
        os.path.join(conda_env_dir, r"Lib\site-packages"),
    ]

    for p in python_paths:
        if os.path.exists(p):
            if p not in sys.path:
                sys.path.append(p)

def main():
    setup_arcgis_complete()

    logger.info("--- Rozpoczynam Test Importów ---")

    # TEST 1: ArcPy
    try:
        # Próba importu
        import arcpy
        logger.success(f"✅ SUKCES! ArcPy załadowany. Wersja: {arcpy.GetInstallInfo()['Version']}")
    except ImportError as e:
        logger.critical(f"❌ BŁĄD IMPORTU: {e}")
        logger.info("🔍 Analiza błędu:")
        if "DLL load failed" in str(e):
            logger.info("   -> Nadal brakuje jakiejś biblioteki DLL w PATH lub add_dll_directory.")
            logger.info("   -> Sprawdź, czy folder 'Library/bin' w katalogu arcgispro-py3 faktycznie istnieje.")
        return
    except Exception as e:
        logger.critical(f"❌ Nieoczekiwany błąd: {e}")
        return

    # TEST 2: GeoPandas
    try:
        import geopandas as gpd
        logger.success(f"✅ GeoPandas załadowany (v{gpd.__version__})")
    except ImportError as e:
        logger.error(f"❌ Błąd GeoPandas: {e}")

if __name__ == "__main__":
    main()