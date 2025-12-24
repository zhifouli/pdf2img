# -*- mode: python ; coding: utf-8 -*-
"""
优化版 PyInstaller 配置文件
通过排除不必要的模块来减小 EXE 体积

版本: V1.0.0
作者: zhifouli
GitHub: https://github.com/zhifouli?tab=repositories
"""

import sys
import os

# 版本信息
VERSION = '1.0.0'
AUTHOR = 'zhifouli'

block_cipher = None

# 排除不必要的模块以减小体积
# 注意: 新版 PyMuPDF (1.24+) 需要 html 模块，不能排除
excludes = [
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'PIL',
    'pillow',
    'pytest',
    'setuptools',
    'distutils',
    'email',
    # 'html',  # PyMuPDF 1.24+ 需要，不能排除
    # 'http',  # 保留，可能被 html 依赖
    # 'urllib',  # 保留，可能被使用
    # 'xml',  # 保留，可能被使用
    'xmlrpc',
    'pydoc',
    'doctest',
    'unittest',
    'test',
    '_pytest',
    'py',
    'pluggy',
]

a = Analysis(
    ['pdf2img_converter.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icon.ico', '.'),  # 将图标文件打包到根目录
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.ttk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
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
    name=f'PDF转图片工具_V{VERSION}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # 启用 strip 减小体积
    upx=True,    # 启用 UPX 压缩
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)
