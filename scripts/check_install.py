from loguru import logger

def main():
    logger.info("--- Test Importów ---")

    # TEST 1: ArcPy
    try:
        import arcpy
        logger.success(f"✅ ArcPy załadowany. Wersja: {arcpy.GetInstallInfo()['Version']}")
    except ImportError as e:
        logger.critical(f"❌ BŁĄD ArcPy: {e}")
        return
    
    # TEST 2: GeoPandas
    try:
        import geopandas as gpd
        logger.success(f"✅ GeoPandas załadowany (v{gpd.__version__})")
    except ImportError as e:
        logger.error(f"❌ Błąd GeoPandas: {e}")
        return
    
    # TEST 3: OSMnx
    try:
        import osmnx as ox
        logger.success(f"✅ OSMnx załadowany (v{ox.__version__})")
    except ImportError as e:
        logger.error(f"❌ Błąd OSMnx: {e}")
        return
    
    logger.success("🎉 Wszystkie pakiety załadowane pomyślnie!")

if __name__ == "__main__":
    main()