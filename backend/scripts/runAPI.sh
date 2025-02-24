#!/bin/bash

VENV_DIR="venv"
# Activate the virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source $VENV_DIR/Scripts/activate  # Windows
else
    source $VENV_DIR/bin/activate  # Linux/macOS
fi

echo "Virtual environment activated."

uvicorn src.main:app --reload