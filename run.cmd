@echo off
clear

:START
echo Starting...
pipenv run python run.py
set EXITCODE=%ERRORLEVEL%

if "%EXITCODE%"=="69" goto START

echo Exited with code: %EXITCODE%
