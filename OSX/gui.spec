# -*- mode: python -*-

block_cipher = None


a = Analysis(['gui.py'],
             pathex=['/Users/wenluwang/Documents/parallel_structure/OSX'],
             binaries=[],
             hiddenimports=['PyQt5.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('img.png','/Users/wenluwang/Documents/parallel_structure/OSX/img.png', "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='gui')
app = BUNDLE(coll,
             name='easyparallel.app',
             icon=None,
             bundle_identifier=None)