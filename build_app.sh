#!/bin/bash
set -euo pipefail

APP_NAME="DaVinci AI Commander"
VERSION="1.0.0"
DMG_NAME="DaVinci-AI-Commander-${VERSION}"

echo "=== Building ${APP_NAME} v${VERSION} ==="

# --- 1. Clean ---
rm -rf build dist "${DMG_NAME}.dmg"

# --- 2. Build with PyInstaller using .spec file ---
pyinstaller --noconfirm "${APP_NAME}.spec"

echo "Build complete: dist/${APP_NAME}.app"

# --- 3. Code signing (optional, requires Developer ID Application cert) ---
if [ -n "${CODESIGN_IDENTITY:-}" ]; then
    echo "=== Signing with: ${CODESIGN_IDENTITY} ==="
    codesign --deep --force --options runtime \
        --entitlements entitlements.plist \
        --sign "${CODESIGN_IDENTITY}" \
        "dist/${APP_NAME}.app"
    echo "Signed."
    codesign --verify --verbose "dist/${APP_NAME}.app"
else
    echo "Skipping code signing (set CODESIGN_IDENTITY to enable)"
fi

# --- 4. Create DMG ---
echo "=== Creating DMG ==="
hdiutil create -volname "${APP_NAME}" \
    -srcfolder "dist/${APP_NAME}.app" \
    -ov -format UDZO \
    "${DMG_NAME}.dmg"
echo "DMG created: ${DMG_NAME}.dmg"

# --- 5. Notarize (optional, requires Apple ID + app-specific password) ---
if [ -n "${CODESIGN_IDENTITY:-}" ] && [ -n "${APPLE_ID:-}" ] && [ -n "${APPLE_TEAM_ID:-}" ]; then
    echo "=== Notarizing ==="
    xcrun notarytool submit "${DMG_NAME}.dmg" \
        --apple-id "${APPLE_ID}" \
        --team-id "${APPLE_TEAM_ID}" \
        --password "${APP_PASSWORD}" \
        --wait
    xcrun stapler staple "${DMG_NAME}.dmg"
    echo "Notarization complete."
else
    echo "Skipping notarization (set APPLE_ID, APPLE_TEAM_ID, APP_PASSWORD to enable)"
fi

echo ""
echo "=== Done ==="
echo "  App: dist/${APP_NAME}.app"
echo "  DMG: ${DMG_NAME}.dmg"
