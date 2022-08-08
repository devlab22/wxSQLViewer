# -*- coding: utf-8 -*-

# cmd/PowerShell C:\python37\python.exe setup.py build

from cx_Freeze import setup, Executable
import subprocess
import sys
import json

print("start")

PACKAGES = ["wxPython"]
INCLUDES = ["MySQLViewer", "sqlite_helper"]
installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8')
installed_packages = installed_packages.split('\r\n')
EXCLUDES = [pkg.split('==')[0] for pkg in installed_packages if pkg != '']
EXCLUDES.append("tkinter")

for pkg in PACKAGES:
    if pkg in EXCLUDES:
        EXCLUDES.remove(pkg)

options = {
    "build.exe": {
        "includes": INCLUDES,
        "packages": PACKAGES,
        "excludes": EXCLUDES,
        "include_msvcr": True,
        "optimize": 2
        
    }
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    
#print(json.dumps(options, indent=4))

#sys.exit(0)

setup(
    name = "SQL Viewer",
    version = "1.0",
    description = "SQL Viewer",
    options = options,
    executables = [Executable(script="main.py", base = base, targetName="SQLViewer.exe")]
)

print("end")