#!/bin/bash

echo "🌐 Setting up Doctor-Patient Communication System..."
set -e  # Exit on any error

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)     PLATFORM="Linux";;
    Darwin*)    PLATFORM="Mac";;
    MINGW*|MSYS*|CYGWIN*) PLATFORM="Windows";;
    *)          echo "❌ Unsupported OS: $OS"; exit 1;;
esac

echo "🖥️ Detected OS: $PLATFORM"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install it and try again."
    exit 1
fi

# Check for virtual environment module
if ! python3 -m venv --help &> /dev/null; then
    echo "❌ 'venv' module not available. Please ensure Python3 includes venv."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "⚙️ Activating virtual environment..."
if [ "$PLATFORM" = "Windows" ]; then
    .venv/Scripts/activate.bat
else
    source .venv/bin/activate
fi

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Please ensure it exists in the current directory."
    deactivate
    exit 1
fi

echo "📚 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo "🔁 Activate the environment using:"
if [ "$PLATFORM" = "Windows" ]; then
    echo "    .venv/Scripts/activate.bat"
else
    echo "    source .venv/bin/activate"
fi
