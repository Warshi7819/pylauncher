REM OLD VERSION FROM 2004
REM Create build spec
python "c:\Program Files\pyinstaller-1.3\Makespec.py" -D -w --icon=images\al_icon.ico Al.py

REM Remove old build directories
rm -rf distAl buildAl

REM compile
python "c:\Program Files\pyinstaller-1.3\Build.py" Al.spec

cd distAl
cp -r ..\icons .
cp -r ..\images .
cp c:\Python25\python.exe.manifest Al.exe.manifest@
