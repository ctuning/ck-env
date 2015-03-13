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

echo.
echo Getting LLVM trunk from SVN

svn co http://llvm.org/svn/llvm-project/llvm/trunk %INSTALL_DIR%\trunk\llvm
svn co http://llvm.org/svn/llvm-project/cfe/trunk  %INSTALL_DIR%\trunk\llvm\tools\clang

echo.
echo Configuring using Visual Studio 2013 ...

set INSTALL_OBJ_DIR=%INSTALL_DIR%\obj
mkdir %INSTALL_OBJ_DIR%

cd /D %INSTALL_OBJ_DIR%

cmake.exe -G "Visual Studio 12 2013" -DCMAKE_INSTALL_PREFIX=%INSTALL_DIR% -DLLVM_TARGETS_TO_BUILD=X86;ARM;NVPTX %INSTALL_DIR%\trunk\llvm

echo.
echo Building using Visual Studio 2013 ...

msbuild.exe llvm.sln
if !errorlevel! neq 0 exit /b !errorlevel! 

exit /b 0
