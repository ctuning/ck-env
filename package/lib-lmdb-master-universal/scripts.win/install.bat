@echo off

rem
rem Extra installation script
rem
rem See CK LICENSE.txt for licensing details.
rem See CK Copyright.txt for copyright details.
rem
rem Developer(s): Grigori Fursin, Daniil Efremov 2016-2017
rem

cd /D %INSTALL_DIR%\src\libraries\liblmdb

mkdir %INSTALL_DIR%\include
copy /B *.h %INSTALL_DIR%\include

echo.
echo Building static library ...
echo.

set CK_TARGET_FILE=lmdb.lib
set CK_TARGET_FILE_S=%CK_TARGET_FILE%

del /Q *.obj
del /Q %CK_TARGET_FILE% 

set CK_SOURCE_FILES=mdb.c midl.c
set CK_OBJ_FILES=mdb.obj midl.obj

set CK_CC_FLAGS=%CK_COMPILER_FLAGS_OBLIGATORY% %CK_COMPILER_FLAGS_MISC% %CK_COMPILER_FLAGS_CC_OPTS% %CK_COMPILER_FLAGS_ARCH% %CK_COMPILER_FLAGS_PAR%

echo Executing %CK_CC% %CK_OPT_SPEED% %CK_FLAGS_STATIC_LIB% %CK_FLAGS_CREATE_OBJ% %CK_CC_FLAGS% %CK_SOURCE_FILES% %CK_LD_FLAGS_MISC% %CK_LD_FLAGS_EXTRA%
%CK_CC% %CK_OPT_SPEED% %CK_FLAGS_STATIC_LIB% %CK_FLAGS_CREATE_OBJ% %CK_CC_FLAGS% %CK_SOURCE_FILES% %CK_LD_FLAGS_MISC% %CK_LD_FLAGS_EXTRA% 
if %errorlevel% neq 0 (
 echo.
 echo Building failed!
 goto err
)

echo Executing %CK_LB% %CK_LB_OUTPUT%%CK_TARGET_FILE% %CK_OBJ_FILES% advapi32.lib ntdll.lib 
%CK_LB% %CK_LB_OUTPUT%%CK_TARGET_FILE% %CK_OBJ_FILES% advapi32.lib ntdll.lib
if %errorlevel% neq 0 (
 echo.
 echo Building failed!
 goto err
)

echo.
echo Installing ...
echo.

mkdir %INSTALL_DIR%\lib
copy /B %CK_TARGET_FILE_S% %INSTALL_DIR%\lib

exit /b 0
