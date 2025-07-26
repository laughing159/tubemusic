#!/bin/bash

# Account Registration Automation Tool - Installation Script
# This script sets up the environment and installs dependencies

set -e

echo "🚀 Setting up Account Registration Automation Tool..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version is installed, but Python $required_version or higher is required."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env configuration file..."
    cp .env.example .env
    echo "✅ Created .env file. You can edit it to customize settings."
fi

# Make main.py executable
chmod +x main.py

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📚 Quick Start:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run test mode: python main.py --test-mode --count 3"
echo "  3. Run actual registration: python main.py --service cursor --count 1"
echo ""
echo "⚠️  REMEMBER: This tool is for educational purposes only!"
echo "    Always respect platform terms of service."
echo ""
echo "📖 For more information, see README.md"