from cx_Freeze import setup, Executable

executables = [Executable("Kraska2D.py",
                          target_name="Kraska2D.exe",
                          base="Win32GUI",
                          icon="icon.ico",
                          shortcut_name="Kraska 2D",
                          shortcut_dir="ProgramMenuFolder")]

excludes = ["unittest", "email", "html", "http", "xml",
            "unicodedata", "bz2", "select"]

include_files = ["pic", "data"]

options = {
    "build_exe": {
        "include_msvcr": True,
        "excludes": excludes,
        "include_files": include_files,
    }
}

setup(name="Kraska 2D",
      version="1.4",
      author="ProgrammX",
      description="Краска 2D - растровый графический редактор",
      executables=executables,
      options=options)