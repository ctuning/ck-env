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
wget http://llvm.org/releases/3.8.0/LLVM-3.8.0-win64.exe

if %errorlevel% neq 0 (
 echo.
 echo Failed installing package!
 goto err
)

call LLVM-3.8.0-win64.exe

if %errorlevel% neq 0 (
 echo.
 echo Failed installing package!
 goto err
)

exit /b 0

:err
exit /b 1
