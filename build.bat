@echo off
REM Build AL and create the installer
REM Requires: pip install wxpython pywin32 pyinstaller, Inno Setup 6
setlocal
set "ROOT=%~dp0"

REM Build the application (must run from src)
pushd "%ROOT%src" || exit /b 1
call compileAl.bat
set "RC=%ERRORLEVEL%"
popd
if not "%RC%"=="0" exit /b %RC%

REM Compile the installer
set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=ISCC.exe"
"%ISCC%" "%ROOT%etc\installerScript.iss"
if errorlevel 1 exit /b 1

echo Installer complete: dist\AL-1.1.0-setup.exe
