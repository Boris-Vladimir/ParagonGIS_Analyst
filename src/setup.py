import sys
from cx_Freeze import setup, Executable
import os

# Run in cmd: python setup.py build

base = None
if sys.platform == "win32":
    base = "Win32GUI"

#buildOptions = dict(include_files = ['fotos/', 'icons/', 'docs/', 'tcl85.dll', 'tk85.dll', 'erros.log'])
buildOptions = dict(include_files = ['icons/', 'data/', 'tcl86t.dll', 'tk86t.dll', 'sqlite3.dll'], 
	packages = ['jdcal']
					)

os.environ['TCL_LIBRARY'] = r'C:\Python34\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python34\tcl\tk8.6'


setup(  name = "Paragon GIS Analyst",
        version = "1.7",
        description = "Simple GUI Application",
        author = "Nuno Venâncio",
        options = dict(build_exe = buildOptions),
        executables = [Executable("pgisaGUI.py", base=base, icon="icons/OpenSignal.ico")])
