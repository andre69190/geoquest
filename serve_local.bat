@echo off
echo ================================================
echo  GeoQuest - Lokaler Test-Server
echo ================================================
echo.

REM Find local IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4"') do (
    set "IP=%%a"
    goto :found
)
:found
set IP=%IP: =%

echo Deine lokale IP-Adresse: %IP%
echo.
echo Starte Server auf Port 8787...
echo.
echo Oeffne auf dem Handy (gleiches WLAN):
echo   http://%IP%:8787
echo.
echo [Strg+C zum Beenden]
echo ================================================
echo.

cd /d "%~dp0"
python -m http.server 8787
pause
