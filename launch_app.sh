#!/bin/bash

# Configuration for DaVinci Resolve Scripting on macOS
export PYTHONPATH="$PYTHONPATH:/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"

# Run the GUI App
# Ensure dependencies are installed (user responsibility, but we can try)
python3 "$(dirname "$0")/app_gui.py"
