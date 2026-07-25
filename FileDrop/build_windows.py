import subprocess
import sys
import os

subprocess.run([
    sys.executable, "-m", "PyInstaller",
    "--name", "FileDrop",
    "--onefile",
    "--windowed",
    "--hidden-import", "qasync",
    "--hidden-import", "qrcode",
    "--hidden-import", "PIL",
    "--add-data", f"file_drop{os.pathsep}file_drop",
    "file_drop/main.py"
], check=True)

print("\nDone! EXE is in dist/FileDrop.exe")