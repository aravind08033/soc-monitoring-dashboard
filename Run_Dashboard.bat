@echo off
title SOC Monitoring Dashboard - Launcher
color 0A
cd /d "%~dp0"

echo ============================================
echo   SOC Monitoring Dashboard - Starting Up
echo ============================================
echo.
echo Step 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://python.org and try again.
    mshta vbscript:Execute("MsgBox ""Python is not installed on this computer.""+chr(10)+""Please install Python from https://python.org and then double-click this launcher again."",vbCritical,""SOC Dashboard - Python Required"":close")
    exit /b
)
echo Python found. OK.
echo.

echo Step 2: Installing required packages (this may take a minute)...
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
echo Packages installed. OK.
echo.

echo Step 3: Launching the dashboard...
echo Your browser will open automatically in a few seconds.
echo (Keep this window open while using the dashboard. Close it when done.)
echo.

start "" /min cmd /c "timeout /t 4 /nobreak >nul && start http://localhost:8501"

python -m streamlit run app.py

pause
