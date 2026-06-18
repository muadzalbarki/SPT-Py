#!/usr/bin/env python3
"""
Build SPT-Py for Windows distribution.

Usage:
    python build_windows.py          # Full build
    python build_windows.py --clean  # Clean + build

Prerequisites (Windows only):
    - Python 3.14+ with all dependencies
    - PyInstaller (pip install pyinstaller)
    - Inno Setup 6 (https://jrsoftware.org/isdl.php)
    - Pillow (pip install Pillow) for icon conversion
"""

import subprocess
import sys
import shutil
import os
from pathlib import Path


def clean():
    for d in ['build', 'dist']:
        shutil.rmtree(d, ignore_errors=True)
    print("✓ Cleaned build/ and dist/")


def build_pyinstaller():
    print("→ Running PyInstaller...")
    result = subprocess.run(
        [sys.executable, '-m', 'PyInstaller',
         'SPT-Py.spec',
         '--clean',
         '--noconfirm'],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print("✗ PyInstaller failed:")
        print(result.stderr)
        sys.exit(1)
    print("✓ PyInstaller build complete")


def build_innosetup():
    iscc_paths = [
        r'C:\Program Files (x86)\Inno Setup 6\ISCC.exe',
        r'C:\Program Files\Inno Setup 6\ISCC.exe',
        r'C:\Program Files (x86)\Inno Setup\ISCC.exe',
    ]
    iscc = None
    for p in iscc_paths:
        if os.path.exists(p):
            iscc = p
            break

    if not iscc:
        print("⚠ Inno Setup not found. Install from https://jrsoftware.org/isdl.php")
        print("  Then manually open installer/setup.iss in Inno Setup.")
        return

    print("→ Running Inno Setup...")
    result = subprocess.run([iscc, 'installer/setup.iss'], capture_output=True, text=True)
    if result.returncode != 0:
        print("✗ Inno Setup failed:")
        print(result.stderr)
        sys.exit(1)
    print("✓ Installer created in installer/")


def convert_icon():
    try:
        from PIL import Image
        img = Image.open('assets/logo.png')
        img.save('installer/icon.ico', format='ICO',
                 sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)])
        print("✓ icon.ico updated")
    except ImportError:
        print("⚠ Pillow not installed. Skipping icon conversion.")


def main():
    if '--clean' in sys.argv:
        clean()

    Path('installer').mkdir(exist_ok=True)
    convert_icon()
    build_pyinstaller()
    build_innosetup()

    output = Path('installer') / 'SPT-Py-Setup.exe'
    if output.exists():
        print(f"\n✅ Build complete: {output.resolve()}")
    else:
        print("\n✅ PyInstaller build complete.")
        print("   Run Inno Setup manually: open installer/setup.iss")


if __name__ == '__main__':
    main()
