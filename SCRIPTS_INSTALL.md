# Davinci AI Commander Scripts Installation

## 1. Quick Install (Script Only)
DaVinci Resolve scripts are simple Python files. You just need to place them in the correct folder.

**Script to Install:** `color_timeline.py` (Vertical Chunk Colorizer)

Run this command in Terminal to copy the script to the DaVinci Resolve Scripts folder:

```zsh
# Run from repository root
cp "color_timeline.py" "$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/"
```

### That's it! 
No restart is usually required, but if it doesn't appear, restart DaVinci Resolve.

## 2. Usage in DaVinci Resolve
1. Open your project/timeline.
2. Go to menu: **Workspace** > **Scripts** > **Utility**.
3. Click **`color_timeline`**.

---

## Technical Details (Optional)
- **Path**: `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility/`
- **Requirements**: Python 3.10.x must be installed on your Mac (see below if you get errors).

### Installing Python 3.10 (If Script doesn't run)
If clicking the script does nothing, you likely need a compatible Python version installed.

```zsh
# Download & Install Python 3.10.11
curl -O https://www.python.org/ftp/python/3.10.11/python-3.10.11-macos11.pkg
sudo installer -pkg "python-3.10.11-macos11.pkg" -target /
```
