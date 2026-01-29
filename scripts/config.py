"""
Konfiguracja projektu porównania budynków OSM vs EGiB
Województwo Mazowieckie
"""
from pathlib import Path

# ===== KATALOGI =====
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = PROJECT_ROOT / "results"

# Automatyczne tworzenie katalogów
for dir_path in [RAW_DIR, PROCESSED_DIR, RESULTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ===== OBSZAR BADANIA =====
# Województwo Mazowieckie - wybrane powiaty do testów
# (pobieranie całego województwa zajęłoby bardzo długo)

STUDY_AREAS = {
    "warszawa_srodmiescie": {
        "name": "Warszawa - Śródmieście",
        "bbox": (20.9800, 52.2100, 21.0500, 52.2500),  # (west, south, east, north)
        "tags": {"building": True},
        "description": "Centrum Warszawy - gęsta zabudowa"
    },
    "piaseczno": {
        "name": "Piaseczno",
        "bbox": (21.0000, 52.0500, 21.1000, 52.1000),
        "tags": {"building": True},
        "description": "Piaseczno - zabudowa podmiejska"
    },
    "legionowo": {
        "name": "Legionowo",
        "bbox": (20.9000, 52.3800, 21.0000, 52.4200),
        "tags": {"building": True},
        "description": "Legionowo - miasto satelickie"
    }
}

# Domyślny obszar badania
DEFAULT_STUDY_AREA = "warszawa_srodmiescie"

# ===== DANE EGIB =====
# Geoportal oferuje WFS z budynkami z bazy BDOT10k
EGIB_WFS_URL = "https://mapy.geoportal.gov.pl/wss/service/PZGIK/BDOT10k/WFS/AdministrativeBoundaries"

# Alternatywne źródło - budynki z BDOT10k przez GUGiK
BDOT_WFS_BUILDINGS = "https://integracja.gugik.gov.pl/cgi-bin/KrajowaIntegracjaEwidencjiGruntow"

# ===== DANE OSM =====
# OSMnx automatycznie pobiera z Overpass API
OSM_CACHE_DIR = RAW_DIR / "osm_cache"
OSM_CACHE_DIR.mkdir(exist_ok=True)

# Tagi budynków do pobrania z OSM
OSM_BUILDING_TAGS = {
    "building": True  # Wszystkie budynki
}

# ===== PARAMETRY PORÓWNANIA =====
# Bufor do sprawdzania nakładania się geometrii (w metrach)
COMPARISON_BUFFER_M = 5.0

# Minimalna powierzchnia budynku do analizy (m²)
MIN_BUILDING_AREA_M2 = 10.0

# Próg podobieństwa geometrii (0-1, gdzie 1 = identyczne)
GEOMETRY_SIMILARITY_THRESHOLD = 0.7

# ===== CRS =====
# EPSG:2180 - układ współrzędnych dla Polski (PUWG 1992)
CRS_POLAND = "EPSG:2180"
# EPSG:4326 - WGS84 (używany przez OSM)
CRS_WGS84 = "EPSG:4326"

# ===== LOGGING =====
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
LOG_FILE = PROJECT_ROOT / "logs" / "pipeline.log"
LOG_FILE.parent.mkdir(exist_ok=True)

# ===== WIZUALIZACJA =====
PLOT_DPI = 150
PLOT_FIGSIZE = (15, 10)
