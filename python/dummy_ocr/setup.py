from cx_Freeze import setup, Executable as cxExecutable
import platform, sys

base = None
if sys.platform == "win32":
    base = "Console"

build_exe_options = {
    "base": base,
    "compressed" : True,
    "create_shared_zip" : True,
    "packages": ["os", "sys", "re", "PIL"],
    "excludes": ["tcl", "Tkconstants", "Tkinter"],
    "include_files" : [
        "patterns/0.png",
        "patterns/1.png",
        "patterns/2.png",
        "patterns/3.png",
        "patterns/4.png",
        "patterns/5.png",
        "patterns/6.png",
        "patterns/7.png",
        "patterns/8.png",
        "patterns/9.png",
        "patterns/dot.png",
        "patterns/colon.png"
    ]
}

WIN_Target = cxExecutable(script = "ocr.py",
    targetName = "ocr.exe",
    compress = True,
    appendScriptToLibrary = False,
    appendScriptToExe = True)

setup(  name = "dummy_ocr",
        version = "0.0.1",
        description = "Dummy OCR 0.0.1",
        options = {"build_exe": build_exe_options},
        executables = [WIN_Target])