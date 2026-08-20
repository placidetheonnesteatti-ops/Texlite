@echo off
setlocal
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m PyInstaller --noconfirm --clean build_windows.spec
if errorlevel 1 exit /b 1
echo.
echo Build termine : dist\Docu2TeX\Docu2TeX.exe
echo.
endlocal
