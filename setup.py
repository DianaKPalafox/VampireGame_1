import sys
from setuptools import setup



APP=['main.py']
DATA_FILES = [('',['images'])]
#OPTIONS = { 'argv_emulation':True}

if sys.platform == 'darwin':
    extra_options = dict(
    setup_requires = ['py2app'],

    app=APP,
    options=dict(py2app=dict(argv_emulation=True)),

)
elif sys.platform == 'win32':
    extra_options =dict(
        setup_requires=['py2exe'],
        app=APP,
    )
else:
    extra_options = dict(
        scripts = APP,
    )
setup(
    name='VampireGame',
    data_files=DATA_FILES,
    **extra_options
)