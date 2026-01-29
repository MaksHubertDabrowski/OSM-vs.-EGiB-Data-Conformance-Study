@echo off
set PYTHON="C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"

if "%1"=="check" (
    %PYTHON% scripts\check_install.py
) else if "%1"=="compare" (
    %PYTHON% scripts\compare_logic.py
) else (
    echo Uzycie: run.bat [check^|compare]
    echo.
    echo Dostepne komendy:
    echo   check   - Sprawdz instalacje pakietow
    echo   compare - Uruchom porownanie danych
)