#!/bin/bash

# Create iconset directory
mkdir app_icon.iconset

# Resizing logic
sips -z 16 16     -s format png app_icon.png --out app_icon.iconset/icon_16x16.png
sips -z 32 32     -s format png app_icon.png --out app_icon.iconset/icon_16x16@2x.png
sips -z 32 32     -s format png app_icon.png --out app_icon.iconset/icon_32x32.png
sips -z 64 64     -s format png app_icon.png --out app_icon.iconset/icon_32x32@2x.png
sips -z 128 128   -s format png app_icon.png --out app_icon.iconset/icon_128x128.png
sips -z 256 256   -s format png app_icon.png --out app_icon.iconset/icon_128x128@2x.png
sips -z 256 256   -s format png app_icon.png --out app_icon.iconset/icon_256x256.png
sips -z 512 512   -s format png app_icon.png --out app_icon.iconset/icon_256x256@2x.png
sips -z 512 512   -s format png app_icon.png --out app_icon.iconset/icon_512x512.png
sips -z 1024 1024 -s format png app_icon.png --out app_icon.iconset/icon_512x512@2x.png

# Create icns file
iconutil -c icns app_icon.iconset

# Cleanup
rm -rf app_icon.iconset
echo "Created app_icon.icns"
