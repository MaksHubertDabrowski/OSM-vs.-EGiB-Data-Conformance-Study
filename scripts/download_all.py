"""
Główny skrypt orkiestrujący cały proces pobierania danych
"""
from loguru import logger
import sys
from pathlib import Path

# Dodaj katalog scripts do PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))
from config import STUDY_AREAS, DEFAULT_STUDY_AREA
from download_osm import download_osm_buildings
from download_egib_v2 import download_egib_buildings

def download_all_data(area_name: str = None):
    """
    Pobiera wszystkie dane (OSM + BDOT10k) dla wybranego obszaru
    
    Args:
        area_name: Nazwa obszaru (None = domyślny)
    """
    if area_name is None:
        area_name = DEFAULT_STUDY_AREA
    
    logger.info("=" * 70)
    logger.info("🚀 START POBIERANIA DANYCH")
    logger.info("=" * 70)
    logger.info(f"Obszar: {STUDY_AREAS[area_name]['name']}")
    logger.info("")
    
    # Krok 1: OSM (szybkie)
    logger.info("KROK 1/2: Pobieranie danych z OpenStreetMap...")
    logger.info("-" * 70)
    try:
        osm_gdf = download_osm_buildings(area_name)
        logger.success(f"✅ OSM: {len(osm_gdf)} budynków")
    except Exception as e:
        logger.error(f"❌ Błąd OSM: {e}")
        return
    
    logger.info("")
    
    # Krok 2: BDOT10k (wolne!)
    logger.info("KROK 2/2: Pobieranie danych z BDOT10k...")
    logger.info("-" * 70)
    logger.warning("⚠️  To może potrwać 5-15 minut! Cierpliwości...")
    try:
        bdot_gdf = download_egib_buildings(area_name)
        logger.success(f"✅ BDOT10k: {len(bdot_gdf)} budynków")
    except Exception as e:
        logger.error(f"❌ Błąd BDOT10k: {e}")
        logger.info("💡 Możesz kontynuować z samymi danymi OSM")
        return
    
    logger.info("")
    logger.info("=" * 70)
    logger.success("🎉 POBIERANIE ZAKOŃCZONE SUKCESEM!")
    logger.info("=" * 70)
    logger.info(f"📊 Podsumowanie dla: {STUDY_AREAS[area_name]['name']}")
    logger.info(f"   OSM:     {len(osm_gdf):,} budynków")
    logger.info(f"   BDOT10k: {len(bdot_gdf):,} budynków")
    logger.info("")
    logger.info("📁 Pliki zapisane w katalogu: data/raw/")
    logger.info("")
    logger.info("➡️  Następny krok: uruchom porównanie")
    logger.info("   python scripts/compare.py")

def main():
    """Główna funkcja z argumentami CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Pobierz dane budynków OSM i BDOT10k",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  python scripts/download_all.py                    # Domyślny obszar
  python scripts/download_all.py --area piaseczno   # Konkretny obszar
  python scripts/download_all.py --list             # Lista dostępnych obszarów
        """
    )
    
    parser.add_argument(
        "--area",
        type=str,
        default=None,
        help=f"Nazwa obszaru (domyślnie: {DEFAULT_STUDY_AREA})"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="Wyświetl dostępne obszary badań"
    )
    
    args = parser.parse_args()
    
    if args.list:
        logger.info("📍 Dostępne obszary badań:")
        for key, area in STUDY_AREAS.items():
            logger.info(f"  • {key:25} - {area['name']}")
            logger.info(f"    {area['description']}")
        return
    
    download_all_data(args.area)

if __name__ == "__main__":
    main()
