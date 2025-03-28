# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('images/enemySample40x40.png', 'images'), ('images/mapSample.png', 'images'), ('sounds/backgroundmusic.mp3', 'sounds'), ('images/high-volume.png','images'),('images/low-volume.png', 'images'), ('images/medium-volume.png', 'images'), ('images/mute.png','images'), ('images/cancel_button.png', 'images'), ('images/mushroom.png', 'images'), ('images/towerSample.png', 'images'),
('images/enemy1/BlueMushroom/bluemushroom0.png', 'images/enemy1/BlueMushroom'), ('images/enemy1/BlueMushroom/bluemushroom1.png', 'images/enemy1/BlueMushroom'), ('images/enemy1/BlueMushroom/bluemushroom2.png', 'images/enemy1/BlueMushroom'), ('images/enemy1/BlueMushroom/bluemushroom3.png', 'images/enemy1/BlueMushroom'), ('images/enemy1/BlueMushroom/bluemushroom4.png', 'images/enemy1/BlueMushroom'), ('images/enemy1/BlueMushroom/bluemushroom5.png', 'images/enemy1/BlueMushroom'), ('images/enemy1/BlueMushroom/bluemushroom6.png', 'images/enemy1/BlueMushroom'), ('images/enemy1/BlueMushroom/bluemushroom7.png', 'images/enemy1/BlueMushroom'), ('images/enemy1/PurpleMushroom/purplemushroom0.png', 'images/enemy1/PurpleMushroom'), ('images/enemy1/PurpleMushroom/purplemushroom1.png', 'images/enemy1/PurpleMushroom'), ('images/enemy1/PurpleMushroom/purplemushroom2.png', 'images/enemy1/PurpleMushroom'), ('images/enemy1/PurpleMushroom/purplemushroom3.png', 'images/enemy1/PurpleMushroom'), ('images/enemy1/PurpleMushroom/purplemushroom4.png', 'images/enemy1/PurpleMushroom'), ('images/enemy1/PurpleMushroom/purplemushroom5.png', 'images/enemy1/PurpleMushroom'), ('images/enemy1/PurpleMushroom/purplemushroom6.png', 'images/enemy1/PurpleMushroom'), ('images/enemy1/PurpleMushroom/purplemushroom7.png', 'images/enemy1/PurpleMushroom'), ('images/enemy1/RedMushroom/redmushroom0.png', 'images/enemy1/RedMushroom'), ('images/enemy1/RedMushroom/redmushroom1.png', 'images/enemy1/RedMushroom'), ('images/enemy1/RedMushroom/redmushroom2.png', 'images/enemy1/RedMushroom'), ('images/enemy1/RedMushroom/redmushroom3.png', 'images/enemy1/RedMushroom'), ('images/enemy1/RedMushroom/redmushroom4.png', 'images/enemy1/RedMushroom'), ('images/enemy1/RedMushroom/redmushroom5.png', 'images/enemy1/RedMushroom'), ('images/enemy1/RedMushroom/redmushroom6.png', 'images/enemy1/RedMushroom'), ('images/enemy1/RedMushroom/redmushroom7.png', 'images/enemy1/RedMushroom'), ('images/glowingmushroom.png', 'images'),
('images/enemy1/GlowingMushroom/glowingmushroom0.png', 'images/enemy1/GlowingMushroom'), ('images/enemy1/GlowingMushroom/glowingmushroom1.png', 'images/enemy1/GlowingMushroom'), ('images/enemy1/GlowingMushroom/glowingmushroom2.png', 'images/enemy1/GlowingMushroom'), ('images/enemy1/GlowingMushroom/glowingmushroom3.png', 'images/enemy1/GlowingMushroom'), ('images/enemy1/GlowingMushroom/glowingmushroom4.png', 'images/enemy1/GlowingMushroom'), ('images/enemy1/GlowingMushroom/glowingmushroom5.png', 'images/enemy1/GlowingMushroom'), ('images/enemy1/GlowingMushroom/glowingmushroom6.png', 'images/enemy1/GlowingMushroom'), ('images/enemy1/GlowingMushroom/glowingmushroom7.png', 'images/enemy1/GlowingMushroom'),
('images/enemy1/RedMushroom/Die/redmushroomdie0.png', 'images/enemy1/RedMushroom/Die'), ('images/enemy1/RedMushroom/Die/redmushroomdie1.png', 'images/enemy1/RedMushroom/Die'), ('images/enemy1/RedMushroom/Die/redmushroomdie2.png', 'images/enemy1/RedMushroom/Die'), ('images/enemy1/RedMushroom/Die/redmushroomdie3.png', 'images/enemy1/RedMushroom/Die'), ('images/enemy1/RedMushroom/Die/redmushroomdie4.png', 'images/enemy1/RedMushroom/Die'), ('images/enemy1/RedMushroom/Die/redmushroomdie5.png', 'images/enemy1/RedMushroom/Die'), ('images/enemy1/RedMushroom/Die/redmushroomdie6.png', 'images/enemy1/RedMushroom/Die'),
('images/enemy1/PurpleMushroom/Die/purplemushroomdie0.png', 'images/enemy1/PurpleMushroom/Die'), ('images/enemy1/PurpleMushroom/Die/purplemushroomdie1.png', 'images/enemy1/PurpleMushroom/Die'), ('images/enemy1/PurpleMushroom/Die/purplemushroomdie2.png', 'images/enemy1/PurpleMushroom/Die'), ('images/enemy1/PurpleMushroom/Die/purplemushroomdie3.png', 'images/enemy1/PurpleMushroom/Die'), ('images/enemy1/PurpleMushroom/Die/purplemushroomdie4.png', 'images/enemy1/PurpleMushroom/Die'), ('images/enemy1/PurpleMushroom/Die/purplemushroomdie5.png', 'images/enemy1/PurpleMushroom/Die'), ('images/enemy1/PurpleMushroom/Die/purplemushroomdie6.png', 'images/enemy1/PurpleMushroom/Die'),
('images/enemy1/BlueMushroom/Die/bluemushroomdie0.png', 'images/enemy1/BlueMushroom/Die'), ('images/enemy1/BlueMushroom/Die/bluemushroomdie1.png', 'images/enemy1/BlueMushroom/Die'), ('images/enemy1/BlueMushroom/Die/bluemushroomdie2.png', 'images/enemy1/BlueMushroom/Die'), ('images/enemy1/BlueMushroom/Die/bluemushroomdie3.png', 'images/enemy1/BlueMushroom/Die'), ('images/enemy1/BlueMushroom/Die/bluemushroomdie4.png', 'images/enemy1/BlueMushroom/Die'), ('images/enemy1/BlueMushroom/Die/bluemushroomdie5.png', 'images/enemy1/BlueMushroom/Die'), ('images/enemy1/BlueMushroom/Die/bluemushroomdie6.png', 'images/enemy1/BlueMushroom/Die'),
('images/enemy1/GlowingMushroom/Die/glowingmushroomdie0.png', 'images/enemy1/GlowingMushroom/Die'), ('images/enemy1/GlowingMushroom/Die/glowingmushroomdie1.png', 'images/enemy1/GlowingMushroom/Die'), ('images/enemy1/GlowingMushroom/Die/glowingmushroomdie2.png', 'images/enemy1/GlowingMushroom/Die'), ('images/enemy1/GlowingMushroom/Die/glowingmushroomdie3.png', 'images/enemy1/GlowingMushroom/Die'), ('images/enemy1/GlowingMushroom/Die/glowingmushroomdie4.png', 'images/enemy1/GlowingMushroom/Die'), ('images/enemy1/GlowingMushroom/Die/glowingmushroomdie5.png', 'images/enemy1/GlowingMushroom/Die'), ('images/enemy1/GlowingMushroom/Die/glowingmushroomdie6.png', 'images/enemy1/GlowingMushroom/Die'),
]
datas += collect_data_files('assets/chars')
datas += collect_data_files('assets/tiles')
datas += collect_data_files('assets/fonts')


a = Analysis(
    ['Main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
