#!/bin/bash

# Install PyInstaller
pip install pyinstaller

# Clean previous builds
rm -rf build dist

# Get path to customtkinter to include it
CUSTOMTKINTER_PATH=$(python3 -c "import customtkinter; print(customtkinter.__path__[0])")

# Run PyInstaller
# --noconfirm: overwrite directory
# --windowed: create .app bundle
# --name: App name
# --add-data: include customtkinter theme files
# --hidden-import: ensure dvr and google.generativeai are found
pyinstaller --noconfirm --windowed \
    --name "DaVinci AI Commander" \
    --add-data "$CUSTOMTKINTER_PATH:customtkinter/" \
    --hidden-import "dvr" \
    --hidden-import "google.generativeai" \
    --hidden-import "PIL" \
    app_gui.py

echo "Build complete. App is in dist/DaVinci AI Commander.app"
