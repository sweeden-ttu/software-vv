#!/bin/bash
# Setup script for the Canvas LMS Blog Template

set -e

echo "=========================================="
echo "Canvas LMS Blog Template Setup"
echo "=========================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check for Ruby
if ! command -v ruby &> /dev/null; then
    echo "Warning: Ruby is not installed. Jekyll setup will be skipped."
    echo "Install Ruby to use the Jekyll blog features."
fi

# Install Python dependencies
echo "Installing Python dependencies..."
if command -v uv &> /dev/null; then
    echo "Using uv package manager..."
    uv pip install -r requirements.txt
else
    echo "Using pip..."
    pip3 install -r requirements.txt
fi

# Install Jekyll dependencies if Ruby is available
if command -v ruby &> /dev/null; then
    echo ""
    echo "Instralling Jekyll dependencies..."
    if command -v bundle &> /dev/null; then
        bundle install
    else
        echo "Warning: Bundler not found. Install it with: gem install bundler"
    fi
fi

# Create .env from example if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp env.example .env
    echo "Please edit .env and add your API keys"
fi

# Check for Kaggle credentials
if [ ! -f ~/.kaggle/kaggle.json ]; then
    echo ""
    echo "Warning: Kaggle API credentials not found."
    echo "Create ~/.kaggle/kaggle.json with your credentials:"
    echo '{"username":"your_username","key":"your_api_key"}'
    echo "Get your API key from: https://www.kaggle.com/account"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Run: python3 agent_setup.py (to configure API keys interactively)"
echo "3. Run: python3 kaggle_agent.py (to validate Kaggle kernels)"
echo "4. Run: bundle exec jekyll serve (to start the blog server)"
echo ""
