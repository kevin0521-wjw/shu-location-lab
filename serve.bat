@echo off
REM LOCATION LAB - start a local static server, then open the browser.
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python not found. You can still open index.html directly by double-clicking it.
  pause
  exit /b 1
)
start "" http://127.0.0.1:8080/
python serve.py %*
pause
