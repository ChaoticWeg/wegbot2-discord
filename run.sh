#!/bin/bash
clear

echo Starting...
python3.6 run.py

exitcode=$?

echo -ne "\nExited with code $exitcode\n"
echo -ne "\nExited with code $exitcode\n\n" >> logs/wegbot.log
