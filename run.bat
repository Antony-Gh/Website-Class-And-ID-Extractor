@echo off
REM Get the path of python3
for /f "tokens=*" %%i in ('where python3') do set PYTHON_PATH=%%i



REM Check if PYTHON_PATH is set
if "%PYTHON_PATH%"=="" (
    for /f "tokens=*" %%i in ('where python') do set PYTHON_PATH=%%i
)

REM Check if PYTHON_PATH is set
if "%PYTHON_PATH%"=="" (
    echo Python3 is not installed or not found in PATH.
    pause
    exit /b 1
)



REM Run the gui.py script located in the same directory as this batch file

%PYTHON_PATH% "%~dp0gui.py"

pause