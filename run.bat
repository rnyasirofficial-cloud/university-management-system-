@echo off
title University Management System (UMS) - SDAA Project
echo ============================================================================
echo   UNIVERSITY MANAGEMENT SYSTEM (UMS)
echo   SDAA Project Proposal Implementation (3NF Database + OOP Architecture)
echo   Group Members:
echo     1. Syed Ali Zaman
echo     2. Muhammad Yasir Ali
echo     3. Muhammad Umer
echo ============================================================================
echo.
echo Starting FastAPI Web Server at http://127.0.0.1:8000 ...
echo.

start "" "http://127.0.0.1:8000"
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
pause
