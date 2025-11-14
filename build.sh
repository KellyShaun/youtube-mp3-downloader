#!/bin/bash
set -o errexit

echo "Installing FFmpeg..."
# Install FFmpeg from package manager
apt-get update
apt-get install -y ffmpeg

# Verify installation
ffmpeg -version

# Install Python dependencies
pip install -r requirements.txt
