@echo off
set PYTHON="C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"

if "%1"=="check" (
    %PYTHON% scripts\check_install.py
) else if "%1"=="compare" (
    %PYTHON% scripts\compare_logic.py
) else if "%1"=="download" (
    %PYTHON% scripts\download_all.py %2 %3 %4
) else if "%1"=="download-osm" (
    %PYTHON% scripts\download_osm.py %2 %3
) else if "%1"=="download-egib" (
    %PYTHON% scripts\download_egib.py %2 %3
) else (
    echo Uzycie: run.bat [komenda] [opcje]
    echo.
    echo Dostepne komendy:
    echo   check             - Sprawdz instalacje pakietow
    echo   compare           - Uruchom porownanie danych
    echo   download          - Pobierz dane OSM i BDOT10k
    echo   download-osm      - Pobierz tylko dane OSM
    echo   download-egib     - Pobierz tylko dane BDOT10k
    echo.
    echo Przyklady:
    echo   run.bat download
    echo   run.bat download --area piaseczno
    echo   run.bat download --list
)
