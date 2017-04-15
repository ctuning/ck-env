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

set LIB_NAME=libOpenCL

echo.
echo Copying OpenCL stubs ...
echo.

mkdir %INSTALL_DIR%\src
mkdir %INSTALL_DIR%\lib
mkdir %INSTALL_DIR%\include
mkdir %INSTALL_DIR%\include\CL

copy /B %PACKAGE_DIR%\lib\stubs.c %INSTALL_DIR%\src
copy /B %PACKAGE_DIR%\ck-make.bat %INSTALL_DIR%\src
copy /B %PACKAGE_DIR%\include\CL\* %INSTALL_DIR%\include\CL
copy /B %PACKAGE_DIR%\README %INSTALL_DIR%

cd %INSTALL_DIR%\src

call ck-make.bat
if %errorlevel% neq 0 (
 echo.
 echo Problem building CK package!
 goto err
)

exit /b 0

:err
exit /b 1
