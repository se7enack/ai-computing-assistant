"""
This setup.py script is for py2applet to build a binary from python source code (Coeus.py)

Usage:
    python3 setup.py py2app
"""

from setuptools import setup

APP = ['Coeus.py']
DATA_FILES = []
OPTIONS = {
    'iconfile':'icon.icns'
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
