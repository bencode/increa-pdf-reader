#!/bin/bash
# PDF Reader MCP Server Installation Script

set -e

echo "🔧 PDF Reader MCP Server Installation"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Check if uv is installed, if so, use it
if command -v uv &> /dev/null; then
    echo "🚀 Using uv for installation (recommended)"
    uv sync --dev
    echo "✅ Installation completed with uv!"
    echo ""
    echo "To run the server:"
    echo "  uv run mcp dev pdf_reader_server.py"
    echo ""
    echo "To install to Claude Code:"
    echo "  uv run mcp install pdf_reader_server.py"
    exit 0
fi

# Fallback to pip + venv
echo "📦 Using pip + venv for installation"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install project in development mode
pip install -e ".[dev]"

echo "✅ Installation completed!"
echo ""
echo "To run the server:"
echo "  source .venv/bin/activate"
echo "  mcp dev pdf_reader_server.py"
echo ""
echo "To install to Claude Code:"
echo "  source .venv/bin/activate"
echo "  mcp install pdf_reader_server.py"