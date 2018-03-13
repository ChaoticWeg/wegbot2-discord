@echo off
clear

set PATH=%PATH%Y:\7-Zip Downloads\ffmpeg-3.4.2-win64-static\bin;

:START
echo Starting...
python run.py

:POST
set EXITCODE=%ERRORLEVEL%
if "%EXITCODE%"=="69" goto START

:DONE
echo Exited with code: %EXITCODE%
