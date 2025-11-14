#!/bin/bash
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Checking for FFmpeg..."
# Check if FFmpeg is available in common locations
if command -v ffmpeg &> /dev/null; then
    echo "FFmpeg found in PATH"
    ffmpeg -version
elif [ -f "/usr/bin/ffmpeg" ]; then
    echo "FFmpeg found at /usr/bin/ffmpeg"
    /usr/bin/ffmpeg -version
elif [ -f "/usr/local/bin/ffmpeg" ]; then
    echo "FFmpeg found at /usr/local/bin/ffmpeg"
    /usr/local/bin/ffmpeg -version
else
    echo "FFmpeg not found. Audio conversion may not work."
fi
