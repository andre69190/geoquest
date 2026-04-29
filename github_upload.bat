@echo off
chcp 65001 >nul
echo =======================================
echo   GeoQuest - Automatischer GitHub Upload
echo =======================================

IF EXIST ".git" GOTO update

:setup
echo.
echo === ERSTES SETUP ===
git init
git branch -M main
set /p repo="Bitte deinen GitHub-Link hier einfuegen (Rechtsklick) und Enter druecken: "
git remote add origin %repo%
git add .
git commit -m "Initiales Setup"
git push -u origin main
GOTO end

:update
echo.
echo === LADE UPDATE HOCH ===
git add .
git commit -m "Auto-Update"
git push

:end
echo.
echo =======================================
echo Erledigt! Deine App ist jetzt auf dem neuesten Stand.
echo Du kannst dieses Fenster jetzt schliessen.
pause