@echo off
clear

:START
echo Starting...
python run.py

:POST
set EXITCODE=%ERRORLEVEL%
if "%EXITCODE%"=="69" goto START

:DONE
echo Exited with code: %EXITCODE%
