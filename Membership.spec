# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.building.build_main import *
import sys
import os
from pathlib import Path

from pylibdmtx import pylibdmtx
from pyzbar import pyzbar

path = os.path.abspath(".")
from kivy_garden import zbarcam

sys.path.insert(0, path)

temp_path = os.path.abspath(zbarcam.__file__)
temp_path = temp_path.split("zbarcam")[0]
print("temp_path = ", temp_path)
zbarcam_path = os.path.split(temp_path)[0]
#print("zbarcam dir =", zbarcam_path)
from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path

zbarcam_data = []

import glob
from os.path import join, dirname, abspath, split
from os import sep
import glob
file_dir = zbarcam.__file__.split("site-packages")
print("__file__ = ", file_dir)
zbarcam_dir = join(file_dir[0], "site-packages", file_dir[1].split(sep)[1])
print("zbarcam_dir =", zbarcam_dir)
zbarcam_data.extend((file, dirname(file).split("site-packages")[1].split(sep, 1)[1]) for file in glob.iglob(join(zbarcam_dir,"**{}*".format(sep)), recursive=True))
print("zbarcam_data = ", zbarcam_data)


a = Analysis(
    ["main.py"],
	pathex=[path],
    binaries=[],
	#datas = zbarcam_data + [("client_secret.json", ".")],
    datas= zbarcam_data + [("assets\\", "assets\\"), ("libs\\", "libs\\")],
    hookspath=[kivymd_hooks_path],
    runtime_hooks=[],
    excludes=["dist", "*.bat", "*.spec", "*.txt", "output"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
	hiddenimports=['pkg_resources.py2_warn','kivy_garden.zbarcam', 'win32file', 'win32timezone' ],
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

a.binaries += TOC([
    (Path(dep._name).name, dep._name, 'BINARY')
    for dep in pylibdmtx.EXTERNAL_DEPENDENCIES + pyzbar.EXTERNAL_DEPENDENCIES
])

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
		  *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='MembershipApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True, icon="club_logo.ico" )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='MembershipApp')