@echo off
SETLOCAL

IF NOT EXIST "venv_win" (
    echo [Windows] Creating virtual environment 'venv_win'...
    python -m venv venv_win
    echo [Windows] Installing dependencies...
    venv_win\Scripts\pip install -r requirements.txt
)

echo [Windows] Starting Application...
venv_win\Scripts\python app.py
