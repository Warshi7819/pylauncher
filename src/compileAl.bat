@echo off
REM Build AL with PyInstaller
REM Run from the src directory. Requires: pip install wxpython pywin32 pyinstaller
setlocal

REM Remove old build directories
if exist buildAl rmdir /s /q buildAl
if exist distAl rmdir /s /q distAl

REM Build with the same python used to run Al.py
python -m PyInstaller --noconfirm --windowed --clean --name Al --icon=images\al_icon.ico --collect-submodules plugins --hidden-import win32timezone --distpath distAl --workpath buildAl Al.py
if errorlevel 1 exit /b 1

REM Copy icons and images next to the exe
xcopy /E /I /Y icons distAl\Al\icons >nul
if errorlevel 1 exit /b 1
xcopy /E /I /Y images distAl\Al\images >nul
if errorlevel 1 exit /b 1

echo Build complete: src\distAl\Al
