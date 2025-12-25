#!/bin/bash

if [ ! -d "venv_linux" ]; then
    echo "[Linux] Creating virtual environment 'venv_linux'..."
    python3 -m venv venv_linux
    echo "[Linux] Installing dependencies..."
    ./venv_linux/bin/pip install -r requirements.txt
fi

echo "[Linux] Starting Application..."
./venv_linux/bin/python app.py
