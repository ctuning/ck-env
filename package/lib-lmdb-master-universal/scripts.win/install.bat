@echo off

rem
rem Extra installation script
rem
rem See CK LICENSE.txt for licensing details.
rem See CK Copyright.txt for copyright details.
rem
rem Developer(s): Grigori Fursin, Daniil Efremov 2016-2017
rem


cd /D %INSTALL_DIR%\%PACKAGE_SUB_DIR%\libraries\liblmdb


############################################################
echo ""
echo "Building package ..."

mingw32-make PREFIX="%INSTALL_DIR%\install" BINARY=%CK_TARGET_CPU_BITS% MAKE=mingw32-make.exe CC=%CK_CC% %CK_COMPILER_FLAGS_OBLIGATORY% AR="%CK_AR%" XCFLAGS="-DMDB_DSYNC=O_SYNC -DMDB_USE_ROBUST=0"

if %errorlevel% neq 0 (
 echo.
 echo Error: make failed!
 goto err
)

mingw32-make install PREFIX="%INSTALL_DIR%\install"

if %errorlevel% neq 0 (
 echo.
 echo Error: make install failed!
 goto err
)

exit /b 0
