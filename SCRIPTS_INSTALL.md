# Davinci AI Commander Scripts Installation

## 1. Prerequisites (Python Setup)
DaVinci Resolve on macOS usually requires a specific version of Python to be installed in the system framework location.
**Python 3.10.x** is recommended.

Run the following commands in Terminal to install Python 3.10.11:

```zsh
# Download installer
curl -O https://www.python.org/ftp/python/3.10.11/python-3.10.11-macos11.pkg

# Install (Requires Admin Password)
sudo installer -pkg python-3.10.11-macos11.pkg -target /
```

## 2. Installing the Scripts
To make the scripts appear in the DaVinci Resolve `Workspace > Scripts` menu, copy them to the Resolve Scripts Utility folder.

### Colorize Timeline Clips
This script colors clips in the active timeline with a rotating pattern of high-contrast colors.

```zsh
# Run this from the repository root
cp "Colorize_Timeline_Clips.py" "$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/"
```

**Note:** If the folder doesn't exist, you may need to open DaVinci Resolve and the Fusion page once, or create it manually.

## 3. Usage
1. Open DaVinci Resolve.
2. Open a Project and a Timeline.
3. Go to top menu: `Workspace` > `Scripts` > `Utility`.
4. Select `Colorize_Timeline_Clips`.
