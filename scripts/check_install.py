import sys
import os
from loguru import logger

# 1. Ręczne wstrzyknięcie ścieżki do ArcPy (jeśli aktywacja Pixi zawiedzie)
arc_path = r"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\Lib\site-packages"
if arc_path not in sys.path:
    sys.path.append(arc_path)

try:
    import arcpy
    import geopandas as gpd
    
    logger.success("✅ Systemy połączone!")
    logger.info(f"ArcPy: {arcpy.GetInstallInfo()['Version']}")
    logger.info(f"GeoPandas: {gpd.__version__}")
    
except ModuleNotFoundError as e:
    logger.error(f"❌ Nadal brakuje modułu: {e}")
    logger.info("Sprawdź, czy ścieżka arc_path w skrypcie jest identyczna z Twoją instalacją ArcGIS Pro.")
except Exception as e:
    logger.error(f"❌ Nieoczekiwany błąd: {e}")