"""
Pobieranie danych o budynkach z OpenStreetMap
Używa biblioteki OSMnx
"""
import osmnx as ox
import geopandas as gpd
from loguru import logger
from pathlib import Path
import sys

# Dodaj katalog scripts do PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    STUDY_AREAS, DEFAULT_STUDY_AREA, RAW_DIR, 
    OSM_BUILDING_TAGS, CRS_POLAND, CRS_WGS84
)

def download_osm_buildings(area_name: str = None) -> gpd.GeoDataFrame:
    """
    Pobiera budynki z OSM dla wybranego obszaru
    
    Args:
        area_name: Nazwa obszaru z config.STUDY_AREAS (None = domyślny)
    
    Returns:
        GeoDataFrame z budynkami
    """
    if area_name is None:
        area_name = DEFAULT_STUDY_AREA
    
    if area_name not in STUDY_AREAS:
        logger.error(f"Nieznany obszar: {area_name}")
        logger.info(f"Dostępne obszary: {list(STUDY_AREAS.keys())}")
        raise ValueError(f"Nieznany obszar: {area_name}")
    
    area = STUDY_AREAS[area_name]
    logger.info(f"📍 Pobieranie danych OSM dla: {area['name']}")
    logger.info(f"   BBox: {area['bbox']}")
    
    try:
        # Konfiguracja OSMnx
        ox.settings.use_cache = True
        ox.settings.cache_folder = str(RAW_DIR / "osm_cache")
        
        # Pobieranie geometrii z OSM
        logger.info("🌍 Łączenie z Overpass API...")
        gdf = ox.features_from_bbox(
            bbox=area['bbox'],
            tags=area['tags']
        )
        
        logger.success(f"✅ Pobrano {len(gdf)} obiektów z OSM")
        
        # Filtrowanie - tylko geometrie typu Polygon/MultiPolygon
        original_count = len(gdf)
        gdf = gdf[gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])]
        logger.info(f"   Budynki (Polygon/MultiPolygon): {len(gdf)}/{original_count}")
        
        # Konwersja CRS do PUWG 1992
        if gdf.crs != CRS_POLAND:
            logger.info(f"🔄 Konwersja CRS: {gdf.crs} → {CRS_POLAND}")
            gdf = gdf.to_crs(CRS_POLAND)
        
        # Dodanie metadanych
        gdf['source'] = 'OSM'
        gdf['area_name'] = area_name
        
        # Obliczanie powierzchni
        gdf['area_m2'] = gdf.geometry.area
        logger.info(f"📊 Statystyki powierzchni:")
        logger.info(f"   Średnia: {gdf['area_m2'].mean():.2f} m²")
        logger.info(f"   Mediana: {gdf['area_m2'].median():.2f} m²")
        logger.info(f"   Min: {gdf['area_m2'].min():.2f} m²")
        logger.info(f"   Max: {gdf['area_m2'].max():.2f} m²")
        
        # Zapis do pliku
        output_path = RAW_DIR / f"osm_buildings_{area_name}.gpkg"
        gdf.to_file(output_path, driver="GPKG")
        logger.success(f"💾 Zapisano do: {output_path}")
        
        return gdf
        
    except Exception as e:
        logger.error(f"❌ Błąd podczas pobierania danych OSM: {e}")
        raise

def main():
    """Główna funkcja - pobiera dane dla wszystkich obszarów lub wybranego"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Pobierz budynki z OSM")
    parser.add_argument(
        "--area",
        type=str,
        default=None,
        help=f"Nazwa obszaru (domyślnie: {DEFAULT_STUDY_AREA})"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Pobierz dane dla wszystkich obszarów"
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("🏗️  POBIERANIE BUDYNKÓW Z OPENSTREETMAP")
    logger.info("=" * 60)
    
    if args.all:
        logger.info(f"Pobieranie dla wszystkich {len(STUDY_AREAS)} obszarów...")
        for area_name in STUDY_AREAS.keys():
            try:
                download_osm_buildings(area_name)
                logger.info("")
            except Exception as e:
                logger.error(f"Błąd dla {area_name}: {e}")
    else:
        download_osm_buildings(args.area)
    
    logger.success("✅ Pobieranie zakończone!")

if __name__ == "__main__":
    main()
