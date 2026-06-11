#!/bin/bash

echo "=== Building App ==="

APP_NAME="Loja_de_Carrinhos"

# Move to the directory where this script is located
cd "$(dirname "$0")"

ENTRY="../../main.py"
DIST_DIR="./dist"
BUILD_DIR="./build"

# Clean previous builds
rm -rf "$BUILD_DIR" "$DIST_DIR" __pycache__
find . -name "__pycache__" -type d -exec rm -rf {} +

# Build onefile
pyinstaller \
    --name "$APP_NAME" \
    --noconfirm \
    --clean \
    --onefile \
    --windowed \
    --distpath "$DIST_DIR" \
    --workpath "$BUILD_DIR" \
    --add-data "../../app/resources/images:app/resources/images" \
    --add-data "../../app/resources/sounds:app/resources/sounds" \
    --add-data "../../app/views:app/views" \
    --add-data "../../app/controllers:app/controllers" \
    --add-data "../../app/services:app/services" \
    --add-data "../../app/models:app/models" \
    --add-data "../../app/core:app/core" \
    "$ENTRY"

# Remove leftover build folder
rm -rf "$BUILD_DIR"

echo "=== Build complete! ==="
echo "Binary available at: $DIST_DIR/$APP_NAME"