@echo off

rem
rem Installation script for CK packages.
rem
rem See CK LICENSE.txt for licensing details.
rem See CK Copyright.txt for copyright details.
rem
rem Developer(s): Grigori Fursin, 2016-2017
rem

cd %INSTALL_DIR%

echo **************************************************************
echo Executing relocation.pl.bat ...
echo .

call relocation.pl.bat

exit /b 0
