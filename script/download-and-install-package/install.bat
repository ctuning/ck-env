@echo off

rem
rem Universal installation script for CK
rem
rem See CK LICENSE.txt for licensing details.
rem See CK Copyright.txt for copyright details.
rem
rem Developer(s): Grigori Fursin, 2016-2017
rem

rem PACKAGE_DIR
rem INSTALL_DIR

cd /D %INSTALL_DIR%

rem ############################################################
set PF=%PACKAGE_URL%/%PACKAGE_NAME%

if "%PACKAGE_WGET%" == "YES" (
  echo.
  echo Downloading package from '%PF%' ...

  if EXIST "%PACKAGE_NAME%" (
    del /Q /S %PACKAGE_NAME%
  )

  wget --no-check-certificate "%PF%"

  if %errorlevel% neq 0 (
   echo.
   echo Error: Failed downloading package ...
   goto err
  )

  if "%PACKAGE_RENAME%" == "YES" (
    ren %PACKAGE_NAME2% %PACKAGE_NAME%
  )
)

if "%PACKAGE_GIT%" == "YES" (
  echo.
  echo Cloning package from '%PF%' ...

  if EXIST "%PACKAGE_SUB_DIR%" (
    rmdir /s /q %PACKAGE_SUB_DIR%
  )

  if EXIST "%PACKAGE_SUB_DIR%" (
    rmdir %PACKAGE_SUB_DIR%
  )

  git clone %PACKAGE_URL% %PACKAGE_SUB_DIR%

  if %errorlevel% neq 0 (
   echo.
   echo Error: git cloning failed ...
   goto err
  )

  if not "%PACKAGE_GIT_CHECKOUT%" == "" (
    cd %PACKAGE_SUB_DIR%

    echo.
    echo Checking out branch %PACKAGE_GIT_CHECKOUT% ...
    echo.
 
    git checkout %PACKAGE_GIT_CHECKOUT%

    if %errorlevel% neq 0 (
     echo.
     echo Error: git checkout failed ...
     goto err
    )
  )
)

rem ############################################################
if "%PACKAGE_UNGZIP%" == "YES" (
  echo.
  echo Ungzipping archive ...

  if EXIST "%PACKAGE_NAME1%" (
    del /Q /S %PACKAGE_NAME1%
  )

  gzip -d %PACKAGE_NAME%

  if %errorlevel% neq 0 (
   echo.
   echo Error: ungzipping package failed!
   goto err
  )
)

rem ############################################################
if "%PACKAGE_UNZIP%" == "YES" (
  echo.
  echo Unzipping archive ...

  unzip -d %PACKAGE_NAME%

  if %errorlevel% neq 0 (
   echo.
   echo Error: unzipping package failed!
   goto err
  )
)

rem ############################################################
if "%PACKAGE_UNBZIP%" == "YES" (
  echo.
  echo Unbzipping archive ...

  if EXIST "%PACKAGE_NAME1%" (
    del /Q /S %PACKAGE_NAME1%
  )

  bzip2 -d %PACKAGE_NAME%

  if %errorlevel% neq 0 (
   echo.
   echo Error: unbzipping package failed!
   goto err
  )
)

rem ############################################################
if "%PACKAGE_UNTAR%" == "YES" (
  echo.
  echo Untarring archive ...

  if EXIST "%PACKAGE_SUB_DIR%" (
    rmdir /s /q %PACKAGE_SUB_DIR%
  )

  if EXIST "%PACKAGE_SUB_DIR%" (
    rmdir %PACKAGE_SUB_DIR%
  )

  tar xvf %PACKAGE_NAME1%

  if NOT "%PACKAGE_UNTAR_SKIP_ERROR_WIN%" == "YES" (
    if %errorlevel% neq 0 (
      echo.
      echo Error: untaring package failed!
      goto err
    )
  )
)

if NOT "%PACKAGE_SKIP_CLEAN_PACKAGE%" == "YES" (
 if EXIST "%PACKAGE_NAME%" (
   del /Q /S %PACKAGE_NAME%
 )
 if EXIST "%PACKAGE_NAME1%" (
   del /Q /S %PACKAGE_NAME1%
 )
)

rem ############################################################
if "%PACKAGE_COPY%" == "YES" (
  if EXIST "%ORIGINAL_PACKAGE_DIR%\copy" (
    echo.
    echo Copying extra files to source dir ...

    xcopy /E %ORIGINAL_PACKAGE_DIR%\copy\* %INSTALL_DIR%\%PACKAGE_SUB_DIR1%
  )

  if EXIST "%ORIGINAL_PACKAGE_DIR%\copy.%CK_TARGET_OS_ID%" (
    echo.
    echo Copying extra files for %CK_TARGET_OS_ID% to source dir ...

    xcopy /E %ORIGINAL_PACKAGE_DIR%\copy.%CK_TARGET_OS_ID%\* %INSTALL_DIR%\%PACKAGE_SUB_DIR1%
  )
)

rem ############################################################
if "%PACKAGE_PATCH%" == "YES" (
  if EXIST "%ORIGINAL_PACKAGE_DIR%\patch.%CK_TARGET_OS_ID%" (
    echo.
    echo Patching source directory ...

    cd /D %INSTALL_DIR%\%PACKAGE_SUB_DIR%

    for /r %ORIGINAL_PACKAGE_DIR%\patch.%CK_TARGET_OS_ID% %%i in (*) do (
      echo %%~fi
      patch -p1 < %%~fi

rem      if %errorlevel% neq 0 (
rem        echo.
rem        echo Error: patching failed!
rem        goto err
      )
    )
  )
)

rem ############################################################
echo.
echo Cleaning ...

cd /D %INSTALL_DIR%

if NOT "%PACKAGE_SKIP_CLEAN_INSTALL%" == "YES" (

  if EXIST install (
    rmdir /s /q install
  )
  if EXIST install (
    rmdir install
  )

)

if NOT "%PACKAGE_SKIP_CLEAN_OBJ%" == "YES" (

  if EXIST obj (
    rmdir /s /q obj
  )
  if EXIST obj (
    rmdir obj
  )

)

if NOT EXIST obj (

  mkdir obj

  if %errorlevel% neq 0 (
    echo.
    echo Error: problem creating obj directory!
    goto err
  )
)

rem ############################################################
if EXIST "%ORIGINAL_PACKAGE_DIR%\scripts.%CK_TARGET_OS_ID%\install.bat" (
  echo.
  echo Executing extra script ...

  call %ORIGINAL_PACKAGE_DIR%\scripts.%CK_TARGET_OS_ID%\install.bat

  if %errorlevel% neq 0 (
   echo.
   echo Error: Failed executing extra script ...
   goto err
  )
)

rem ############################################################
cd /D %INSTALL_DIR%/obj

rem Checking target
set XTARGET=--target install
if not "%PACKAGE_CMAKE_TARGET%" == "" (
  set XTARGET=--target %PACKAGE_CMAKE_TARGET%
)
if "%PACKAGE_SKIP_CMAKE_TARGET%" == "YES" (
  set XTARGET=
)

rem Checking AR
set XCMAKE_AR=
if not "%CK_AR_PATH_FOR_CMAKE%" == "" (
 set XCMAKE_AR=-DCMAKE_AR="%CK_AR_PATH_FOR_CMAKE%"
)

rem Checking LD
set XCMAKE_LD=
if not "%CK_LD_PATH_FOR_CMAKE%" == "" (
 set XCMAKE_LD=-DCMAKE_LD="%CK_LD_PATH_FOR_CMAKE%"
)

rem Checking C flags
set XCMAKE_C_FLAGS=
if not "%CK_CC_FLAGS_FOR_CMAKE% %CK_CC_FLAGS_ANDROID_TYPICAL%" == " " (
 set XCMAKE_C_FLAGS=-DCMAKE_C_FLAGS="%CK_CC_FLAGS_FOR_CMAKE% %CK_CC_FLAGS_ANDROID_TYPICAL%"
)

rem Checking CXX flags
set XCMAKE_CXX_FLAGS=
if not "%CK_CXX_FLAGS_FOR_CMAKE% %CK_CXX_FLAGS_ANDROID_TYPICAL%" == " " (
  set XCMAKE_CXX_FLAGS=-DCMAKE_CXX_FLAGS="%CK_CXX_FLAGS_FOR_CMAKE% %CK_CXX_FLAGS_ANDROID_TYPICAL%"
)

set XCMAKE_EXE_LINKER_FLAGS=
if "%CK_TARGET_OS_ID%" == "android" (
  set XCMAKE_EXE_LINKER_FLAGS=-DCMAKE_EXE_LINKER_FLAGS="%CK_LINKER_FLAGS_ANDROID_TYPICAL%"
)
set XCMAKE_EXE_LINKER_LIBS=
if "%CK_TARGET_OS_ID%" == "android" (
  set XCMAKE_EXE_LINKER_LIBS=-DCMAKE_EXE_LINKER_LIBS="%CK_LINKER_LIBS_ANDROID_TYPICAL%" \
)

if "%PACKAGE_BUILD_TYPE%" == "cmake" (

  echo.
  echo CMake configure flags:
  echo.
  echo %PACKAGE_CONFIGURE_FLAGS% %CK_CMAKE_EXTRA%
  echo.

  rem ############################################################
  echo.
  echo Configuring ...

  cmake -DCMAKE_INSTALL_PREFIX="%INSTALL_DIR%\install" ^
        -DCMAKE_BUILD_TYPE:STRING=%CMAKE_CONFIG% ^
        %PACKAGE_CONFIGURE_FLAGS% ^
        -DCMAKE_C_COMPILER="%CK_CC_PATH_FOR_CMAKE%" ^
        %XCMAKE_C_FLAGS% ^
        -DCMAKE_CXX_COMPILER="%CK_CXX_PATH_FOR_CMAKE%" ^
        %XCMAKE_CXX_FLAGS% ^
        -DCMAKE_AR="%CK_AR_PATH_FOR_CMAKE%" ^
        -DCMAKE_LINKER="%CK_LD_PATH_FOR_CMAKE%" ^
        %XCMAKE_AR% ^
        %XCMAKE_LD% ^
        %XCMAKE_EXE_LINKER_FLAGS% ^
        %XCMAKE_EXE_LINKER_LIBS% ^
        %CK_CMAKE_EXTRA% ^
        %INSTALL_DIR%\%PACKAGE_SUB_DIR1%

  echo **************************************************************
  echo.
  echo Building using Visual Studio ...

  cmake --build . --config %CMAKE_CONFIG% %XTARGET%

  if not "%PACKAGE_SKIP_BUILD_ERROR%" == "YES" (
    if %errorlevel% neq 0 (
     echo.
     echo Problem building CK package!
     goto err
    )
  )
)

rem ############################################################
if EXIST "%ORIGINAL_PACKAGE_DIR%\scripts.%CK_TARGET_OS_ID%\post-install.bat" (
  echo.
  echo Executing extra script ...

  call %ORIGINAL_PACKAGE_DIR%\scripts.%CK_TARGET_OS_ID%\post-install.bat

  if %errorlevel% neq 0 (
   echo.
   echo Error: Failed executing extra script ...
   goto err
  )
)

rem  ############################################################
if NOT "%PACKAGE_SKIP_CLEAN_OBJ_DIR%" == "YES" (
  echo.
  echo Cleaning obj directory ...

  if EXIST obj (
    rmdir /s /q obj
  )
  if EXIST obj (
    rmdir obj
  )
)

rem  ############################################################
rem  CAREFUL - when GIT, CK can't afterwards go to this dir to get revision number ...

rem if NOT "%PACKAGE_SKIP_CLEAN_SRC_DIR%" == "YES" (
rem  echo.
rem  echo Cleaning src directory ...
rem
rem   if EXIST src (
rem    rmdir /s /q src
rem  )
rem  if EXIST src (
rem    rmdir src
rem  )
)

exit /b 0

:err
exit /b 1
