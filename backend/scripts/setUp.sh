#!/bin/bash

# Define the Python version and virtual environment directory
PYTHON_VERSION="python"
VENV_DIR="venv"

echo "Setting up the virtual environment..."

# Create virtual environment if it does not exist
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_VERSION -m venv $VENV_DIR
    echo "Virtual environment created in $VENV_DIR."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source $VENV_DIR/Scripts/activate  # Windows
else
    source $VENV_DIR/bin/activate  # Linux/macOS
fi

echo "Virtual environment activated."

# Upgrade pip
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found! Skipping package installation."
fi

echo "Setup complete. Virtual environment is ready."
