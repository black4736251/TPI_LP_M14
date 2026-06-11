from pathlib import Path
import PyInstaller.__main__

ROOT = Path(__file__).resolve().parents[2]

ENTRY = ROOT / "main.py"

PyInstaller.__main__.run([
    f'--name=Loja_de_Carrinhos',
    '--noconfirm',
    '--clean',
    '--onefile',
    '--windowed',
    f'--distpath={ROOT / "builds/windows/dist"}',
    f'--workpath={ROOT / "builds/windows/build"}',
    f'--add-data={ROOT / "app/resources/images"};app/resources/images',
    f'--add-data={ROOT / "app/resources/sounds"};app/resources/sounds',
    f'--add-data={ROOT / "app/views"};app/views',
    f'--add-data={ROOT / "app/controllers"};app/controllers',
    f'--add-data={ROOT / "app/services"};app/services',
    f'--add-data={ROOT / "app/models"};app/models',
    f'--add-data={ROOT / "app/core"};app/core',
    str(ENTRY)
])