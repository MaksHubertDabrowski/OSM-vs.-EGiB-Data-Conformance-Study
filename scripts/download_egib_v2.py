"""
Pobieranie danych o budynkach z bazy BDOT10k (EGiB)

UWAGA: Oficjalne serwisy WFS często nie działają.
Ten skrypt pobiera dane z oficjalnych plików ZIP GUGiK w formacie GPKG.
"""
import geopandas as gpd
from loguru import logger
from pathlib import Path
import sys
import requests
import zipfile
import tempfile

# Dodaj katalog scripts do PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    STUDY_AREAS, DEFAULT_STUDY_AREA, RAW_DIR,
    CRS_POLAND, CRS_WGS84
)

# Kody TERYT powiatów dla obszarów badań
COUNTY_CODES = {
    "warszawa_srodmiescie": "1465",  # m.st. Warszawa
    "piaseczno": "1418",             # Powiat piaseczyński
    "legionowo": "1408"              # Powiat legionowski
}

def download_egib_buildings(area_name: str = None, use_local: str = None) -> gpd.GeoDataFrame:
    """
    Pobiera budynki z BDOT10k dla wybranego obszaru
    
    Args:
        area_name: Nazwa obszaru z config.STUDY_AREAS (None = domyślny)
        use_local: Ścieżka do lokalnego pliku z budynkami (opcjonalne)
    
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
    logger.info(f"📍 Pobieranie danych referencyjnych dla: {area['name']}")
    logger.info(f"   BBox: {area['bbox']}")
    
    # Jeśli użytkownik podał lokalny plik
    if use_local and Path(use_local).exists():
        return load_local_buildings(use_local, area)
    
    # Pobieranie z GUGiK (BDOT10k GPKG)
    logger.info("💡 Pobieranie danych BDOT10k z GUGiK...")
    
    try:
        county_code = COUNTY_CODES.get(area_name)
        if not county_code:
            raise ValueError(f"Brak kodu powiatu dla {area_name}")
        
        # URL do ZIP z GPKG
        zip_url = f"https://opendata.geoportal.gov.pl/bdot10k/schemat2021/GPKG/14/{county_code}_GPKG.zip"
        logger.info(f"   URL: {zip_url}")
        
        # Pobierz ZIP
        response = requests.get(zip_url)
        response.raise_for_status()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = Path(tmpdir) / f"{county_code}_GPKG.zip"
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            logger.info("✅ Pobrano ZIP")
            
            # Rozpakuj
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
            logger.info("✅ Rozpakowano ZIP")
            
            # Znajdź plik GPKG
            gpkg_files = list(Path(tmpdir).glob("*.gpkg"))
            if not gpkg_files:
                raise FileNotFoundError("Brak pliku GPKG w ZIP")
            gpkg_path = gpkg_files[0]
            logger.info(f"   GPKG: {gpkg_path.name}")
            
            # Wczytaj warstwę budynków (BUBD_A - budynki)
            gdf = gpd.read_file(gpkg_path, layer="BUBD_A")
            logger.success(f"✅ Wczytano {len(gdf)} budynków z BDOT10k")
            
            return finalize_data(gdf, area_name, area)

    except Exception as e:
        logger.warning(f"⚠️ Pobieranie BDOT10k nie powiodło się: {e}")
    
    # Fallback: Użyj budynków OSM jako danych referencyjnych
    logger.info("Metoda fallback: Użycie budynków OSM jako danych referencyjnych")
    logger.info("   (To nie są oficjalne dane BDOT, ale pozwolą na porównanie)")
    
    try:
        import osmnx as ox
        
        ox.settings.use_cache = True
        ox.settings.cache_folder = str(RAW_DIR / "osm_cache")
        
        # Pobierz wszystkie budynki
        gdf = ox.features_from_bbox(
            bbox=area['bbox'],
            tags={'building': True}
        )
        
        logger.success(f"✅ Pobrano {len(gdf)} budynków z OSM")
        return finalize_data(gdf, area_name, area, source='OSM_REFERENCE')
        
    except Exception as e:
        logger.error(f"❌ Wszystkie metody zawiodły: {e}")
        raise

def load_local_buildings(filepath: str, area: dict) -> gpd.GeoDataFrame:
    """Wczytuje budynki z lokalnego pliku"""
    logger.info(f"📂 Wczytywanie lokalnego pliku: {filepath}")
    
    from shapely.geometry import box
    
    # Wczytaj dane
    gdf = gpd.read_file(filepath)
    logger.success(f"✅ Wczytano {len(gdf)} obiektów")
    
    # Przytnij do bbox obszaru
    west, south, east, north = area['bbox']
    bbox_geom = box(west, south, east, north)
    
    # Konwersja do WGS84 jeśli potrzebne
    if gdf.crs != CRS_WGS84:
        gdf = gdf.to_crs(CRS_WGS84)
    
    # Filtruj po bbox
    gdf = gdf[gdf.geometry.intersects(bbox_geom)]
    logger.info(f"   Po filtrowaniu bbox: {len(gdf)} budynków")
    
    return gdf

def finalize_data(gdf: gpd.GeoDataFrame, area_name: str, area: dict, source: str = 'BDOT10k') -> gpd.GeoDataFrame:
    """Finalizuje dane - filtruje, przetwarza, zapisuje"""
    
    if len(gdf) == 0:
        logger.warning("⚠️  Brak budynków w tym obszarze!")
        return gpd.GeoDataFrame()
    
    # Filtrowanie - tylko geometrie typu Polygon/MultiPolygon
    original_count = len(gdf)
    gdf = gdf[gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])]
    logger.info(f"   Budynki (Polygon/MultiPolygon): {len(gdf)}/{original_count}")
    
    # Konwersja CRS do PUWG 1992
    if gdf.crs != CRS_POLAND:
        logger.info(f"🔄 Konwersja CRS: {gdf.crs} → {CRS_POLAND}")
        gdf = gdf.to_crs(CRS_POLAND)
    
    # Dodanie metadanych
    gdf['source'] = source
    gdf['area_name'] = area_name
    
    # Obliczanie powierzchni
    gdf['area_m2'] = gdf.geometry.area
    logger.info(f"📊 Statystyki powierzchni:")
    logger.info(f"   Średnia: {gdf['area_m2'].mean():.2f} m²")
    logger.info(f"   Mediana: {gdf['area_m2'].median():.2f} m²")
    logger.info(f"   Min: {gdf['area_m2'].min():.2f} m²")
    logger.info(f"   Max: {gdf['area_m2'].max():.2f} m²")
    
    # Zapis do pliku
    output_filename = f"reference_buildings_{area_name}.gpkg"
    if source != 'BDOT10k':
        output_filename = f"osm_reference_{area_name}.gpkg"
    
    output_path = RAW_DIR / output_filename
    gdf.to_file(output_path, driver="GPKG")
    logger.success(f"💾 Zapisano do: {output_path}")
    
    return gdf

def main():
    """Główna funkcja - pobiera dane dla wszystkich obszarów lub wybranego"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Pobierz budynki referencyjne (BDOT10k lub OSM)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  python scripts/download_egib.py                           # Domyślny obszar
  python scripts/download_egib.py --area piaseczno          # Konkretny obszar
  python scripts/download_egib.py --local buildings.shp     # Z lokalnego pliku
        """
    )
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
    parser.add_argument(
        "--local",
        type=str,
        default=None,
        help="Ścieżka do lokalnego pliku z budynkami"
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("🏛️  POBIERANIE BUDYNKÓW REFERENCYJNYCH")
    logger.info("=" * 60)
    
    if args.all:
        logger.info(f"Pobieranie dla wszystkich {len(STUDY_AREAS)} obszarów...")
        for area_name in STUDY_AREAS.keys():
            try:
                download_egib_buildings(area_name, args.local)
                logger.info("")
            except Exception as e:
                logger.error(f"Błąd dla {area_name}: {e}")
    else:
        download_egib_buildings(args.area, args.local)
    
    logger.success("✅ Pobieranie zakończone!")

if __name__ == "__main__":
    main()