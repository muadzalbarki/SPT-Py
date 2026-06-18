# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

datas = []
for pattern, dest in [
    ("templates/*.docx", "templates"),
    ("assets/*.png", "assets"),
    ("assets/fonts/**", "assets/fonts"),
    ("assets/pdfjs/**", "assets/pdfjs"),
]:
    for f in Path().glob(pattern):
        datas.append((str(f), dest))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'sqlalchemy',
        'sqlalchemy.sql.default',
        'sqlalchemy.ext.declarative',
        'lxml.etree',
        'lxml._elementpath',
        'pandas',
        'pandas._libs',
        'openpyxl',
        'docx',
        'docxtpl',
        'qtawesome',
        'PySide6.QtWebEngineWidgets',
        'win32com',
        'win32com.client',
        'win32com.client.gencache',
    ],
    excludes=[
        'tkinter',
        'matplotlib',
        'PIL',
        'cv2',
        'numpy.random',
        'scipy',
        'cryptography',
    ],
    hookspath=[],
    runtime_hooks=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SPT-Py',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='installer/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='SPT-Py',
)
