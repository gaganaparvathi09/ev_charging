#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install tkinter for Python
apt-get update
apt-get install -y python3-tk

# If you have other dependencies
pip install -r requirements.txt
