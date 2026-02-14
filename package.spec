# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['reverseEngineerUI.py'],  # ← Change this to your main UI file name
    pathex=[],
    binaries=[],
    datas=[
        ('IngredientDeconstruction.py', '.'),     # ← Change to your backend file name
        ('ingreds_dict.json', '.'),    # ← Change to your first JSON file name
        ('ingreds_ids_map.json', '.'),      # ← Change to your second JSON file name
    ],
    hiddenimports=['multiprocessing', 'multiprocessing.spawn'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MyApp',  # ← Change this to your app name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # ← Change to True if you want to see errors
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
