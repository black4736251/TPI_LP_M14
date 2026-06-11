Write-Host "=== Building App==="

$APP_NAME = "Loja_de_Carrinhos"

# Move to the directory where this script is located
Set-Location -Path $PSScriptRoot

$ENTRY = "..\..\main.py"
$DIST_DIR = ".\dist"
$BUILD_DIR = ".\build"

# Clean previous builds
Remove-Item -Recurse -Force $BUILD_DIR, $DIST_DIR -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force

# Build onefile
pyinstaller `
    --name "$APP_NAME" `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --distpath "$DIST_DIR" `
    --workpath "$BUILD_DIR" `
    --add-data "..\..\app\resources\images;app/resources/images" `
    --add-data "..\..\app\resources\sounds;app/resources/sounds" `
    --add-data "..\..\app\views;app/views" `
    --add-data "..\..\app\controllers;app/controllers" `
    --add-data "..\..\app\services;app/services" `
    --add-data "..\..\app\models;app/models" `
    --add-data "..\..\app\core;app/core" `
    "$ENTRY"

# Remove leftover build folder
Remove-Item -Recurse -Force $BUILD_DIR -ErrorAction SilentlyContinue

Write-Host "=== Build complete! ==="
Write-Host "Binary available at: $DIST_DIR\$APP_NAME.exe"