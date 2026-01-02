@echo off
REM Backend startup script for Windows

setlocal enabledelayedexpansion

echo.
echo Policy Bias Detector - Backend Startup
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✓ Python %python_version%
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Dependencies installed
) else (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Check .env file
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env >nul
    echo.
    echo WARNING: Please edit .env and add your GROQ_API_KEY
    echo Get your API key from: https://console.groq.com/keys
    echo Then run this script again
    pause
    exit /b 1
)

REM Start the application
echo.
echo Starting Policy Bias Detector Backend...
echo ========================================
echo.
echo API Server: http://localhost:5000
echo Health Check: http://localhost:5000/api/health
echo.

python main.py
pause
