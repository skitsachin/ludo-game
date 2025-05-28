import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["pygame"],
    "include_files": []
}

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Ludo Game",
    version="1.0",
    description="A Ludo board game with graphics",
    options={"build_exe": build_exe_options},
    executables=[Executable("ludo_game.py", base=base, icon="icon.ico")]
)
