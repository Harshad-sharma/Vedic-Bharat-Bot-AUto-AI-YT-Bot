@echo off
title Vedic Bharat AI - Auto Pilot Mode
color 0A

echo ==================================================
echo      SYSTEM BOOTING... WAITING FOR INTERNET
echo ==================================================
echo.
echo Waiting 60 seconds for Wi-Fi to connect...
timeout /t 60 /nobreak >nul

echo.
echo [1] Activating Environment...
cd /d D:\Vedic_AI_Bot
call venv\Scripts\activate

echo [2] Checking Dependencies...
pip install schedule instagrapi >nul 2>&1

echo [3] Launching Daily Production (6 Videos)...
python daily_batch.py

echo.
echo ==================================================
echo      BATCH COMPLETE. CLOSING IN 30 SECONDS...
echo ==================================================
timeout /t 30
exit