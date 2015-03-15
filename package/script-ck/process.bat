@echo off

rem
rem Installation script for CK packages.
rem
rem See CK LICENSE.txt for licensing details.
rem See CK Copyright.txt for copyright details.
rem
rem Developer(s): Grigori Fursin, 2015
rem

rem PACKAGE_DIR
rem INSTALL_DIR

cd %INSTALL_DIR%
unzip %PACKAGE_DIR%\script-ck-1.0.zip
if %errorlevel% neq 0 (
 echo Failed extracting package archive!
 set /p x=Press any key to continue!
 exit /b %errorlevel%
)
