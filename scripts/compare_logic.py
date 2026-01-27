import arcpy
import geopandas as gpd
from loguru import logger

def main():
    logger.info("Sprawdzam połączenie ze środowiskiem...")
    
    # Test ArcPy
    install_info = arcpy.GetInstallInfo()
    logger.success(f"Silnik ArcGIS: {install_info['ProductName']} {install_info['Version']}")
    
    # Test GeoPandas (zainstalowanego przez Pixi)
    logger.info(f"GeoPandas version: {gpd.__version__}")
    
    print("\n--- Środowisko skonfigurowane poprawnie! ---")

if __name__ == "__main__":
    main()