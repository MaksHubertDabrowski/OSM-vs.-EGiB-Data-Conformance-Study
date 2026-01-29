# 🏗️ Pobieranie Danych - OSM vs EGiB (Mazowieckie)

Skrypty do automatycznego pobierania danych o budynkach z OpenStreetMap i bazy BDOT10k dla województwa mazowieckiego.

## 📋 Wymagania

Wszystko już zainstalowane! ✅

- Python 3.13 (z ArcGIS Pro)
- geopandas, osmnx, pyogrio, loguru

## 🚀 Szybki Start

### 1. Pobierz dane dla domyślnego obszaru (Warszawa Śródmieście)

```bash
.\run.bat download
```

Lub bezpośrednio:

```bash
& "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" scripts\download_all.py
```

### 2. Zobacz dostępne obszary

```bash
& "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" scripts\download_all.py --list
```

Dostępne obszary:
- `warszawa_srodmiescie` - Centrum Warszawy (gęsta zabudowa)
- `piaseczno` - Piaseczno (zabudowa podmiejska)
- `legionowo` - Legionowo (miasto satelickie)

### 3. Pobierz dane dla konkretnego obszaru

```bash
& "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" scripts\download_all.py --area piaseczno
```

## 📁 Struktura Danych

Po pobraniu dane znajdziesz w:

```
data/
├── raw/                                    # Surowe dane
│   ├── osm_buildings_warszawa_srodmiescie.gpkg
│   ├── bdot_buildings_warszawa_srodmiescie.gpkg
│   └── osm_cache/                          # Cache OSM
└── processed/                              # Przetworzone dane (później)
```

## 🔧 Osobne Skrypty

Jeśli chcesz pobierać dane osobno:

### Tylko OSM (szybkie - ~10 sekund)

```bash
& "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" scripts\download_osm.py
```

### Tylko BDOT10k (wolne - 5-15 minut!)

```bash
& "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" scripts\download_egib.py
```

⚠️ **UWAGA:** Pobieranie z WFS jest bardzo wolne! Serwisy GUGiK czasem są przeciążone.

## 📊 Czego Się Spodziewać

### Warszawa Śródmieście
- OSM: ~3,000-5,000 budynków
- BDOT10k: ~2,000-4,000 budynków
- Czas pobierania: 10-15 minut

### Piaseczno
- OSM: ~1,000-2,000 budynków
- BDOT10k: ~800-1,500 budynków
- Czas pobierania: 5-10 minut

### Legionowo
- OSM: ~500-1,000 budynków
- BDOT10k: ~400-800 budynków
- Czas pobierania: 5-10 minut

## ⚠️ Znane Problemy

1. **WFS jest wolny** - To normalne. Serwisy GUGiK nie są zoptymalizowane pod dużą ilość żądań.
2. **Timeout** - Jeśli połączenie się zrywa, spróbuj ponownie lub zmniejsz obszar.
3. **Brak danych BDOT10k** - Niektóre obszary mogą nie mieć danych. To zależy od aktualności bazy.

## 🔍 Weryfikacja Danych

Po pobraniu możesz sprawdzić dane w QGIS:

1. Otwórz QGIS
2. Dodaj warstwę → Plik → `.gpkg`
3. Wybierz plik z `data/raw/`

## ➡️ Następne Kroki

Po pobraniu danych:

1. **Preprocessing** - Czyszczenie i ujednolicenie danych
2. **Porównanie** - Analiza zgodności geometrii
3. **Wizualizacja** - Mapy rozbieżności

## 💡 Tips

- Zacznij od małego obszaru (Legionowo)
- Dla całego województwa rozważ podzielenie na powiaty
- Cache OSM przyspieszy kolejne pobieranie
- Regularnie backupuj dane

## 🆘 Problemy?

Jeśli coś nie działa:

1. Sprawdź połączenie z internetem
2. Zweryfikuj czy serwisy WFS działają: https://mapy.geoportal.gov.pl
3. Przeczytaj logi - są tam szczegółowe komunikaty
4. Zmniejsz obszar badania

## 📝 Konfiguracja

Wszystkie ustawienia znajdziesz w `scripts/config.py`:
- Obszary badań
- URL do WFS
- Parametry CRS
- Ścieżki katalogów



pip install requests