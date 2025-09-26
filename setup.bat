@echo off
echo ================================================================
echo 🧠💼 DevMatch AI - Windows Setup
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Run the Python setup script
echo 🚀 Running setup script...
python setup.py

if errorlevel 1 (
    echo.
    echo ❌ Setup failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo 🎉 Setup Complete! 
echo ================================================================
echo.
echo To start DevMatch AI:
echo   1. Double-click 'start.bat' or
echo   2. Run 'python app.py' in this folder
echo.
echo The application will open at http://localhost:8080
echo.
pause