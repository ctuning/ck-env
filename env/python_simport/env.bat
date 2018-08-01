@echo off

rem Finding the path to the directory that contains THIS batch script,
rem the solution borrowed from here:
rem       https://stackoverflow.com/questions/8797983/can-a-windows-batch-file-determine-its-own-file-name
rem       https://stackoverflow.com/questions/778135/how-do-i-get-the-equivalent-of-dirname-in-a-batch-file/778147

set PATH_TO_THIS_ENTRY_DIR=%~dp0
set TRIMMED_PATH=%PATH_TO_THIS_ENTRY_DIR:~0,-1%
for /f %j in ("%TRIMMED_PATH%") do set ALREADY_LOADED_NAME=CK_STATIC_ENV_%~nxj

echo %ALREADY_LOADED_NAME%

if not [%1] == [1] (if defined %ALREADY_LOADED_NAME% exit /b 0)

echo Adding %PATH_TO_THIS_ENTRY_DIR% to the PYTHONPATH ...

set PYTHONPATH=%PATH_TO_THIS_ENTRY_DIR%;%PYTHONPATH%

set %ALREADY_LOADED_NAME%=1

exit /b 0
