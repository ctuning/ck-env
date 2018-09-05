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
rem Check if need to substitute ORIGINAL_PACKAGE_DIR with some other location
if not "%SUBSTITUTE_ORIGINAL_PACKAGE_DIR%" == "" (
   set ORIGINAL_PACKAGE_DIR=%SUBSTITUTE_ORIGINAL_PACKAGE_DIR%
   echo Using scripts from %ORIGINAL_PACKAGE_DIR%
)

rem ############################################################
if EXIST "%ORIGINAL_PACKAGE_DIR%\scripts.%CK_TARGET_OS_ID%\pre-download.bat" (
  echo.
  echo Executing pre-download script ...
  echo.

  call %ORIGINAL_PACKAGE_DIR%\scripts.%CK_TARGET_OS_ID%\pre-download.bat

  if %errorlevel% neq 0 (
   echo.
   echo Error: Failed executing pre-download script ...
   goto err
  )
)

rem ############################################################
rem Detect proper names
if "%PACKAGE_DETECT_VARS%" == "YES" (
  if "%CK_TARGET_OS_ID%" == "android" (

    if not "%PACKAGE_URL_WINDOWS_ANDROID%" == "" (
       set PACKAGE_URL=%PACKAGE_URL_WINDOWS_ANDROID%
    )
    if not "%PACKAGE_NAME_WINDOWS_ANDROID%" == "" (
       set PACKAGE_NAME=%PACKAGE_NAME_WINDOWS_ANDROID%
    )
    if not "%PACKAGE_UNGZIP_WINDOWS_ANDROID%" == "" (
       set PACKAGE_UNGZIP=%PACKAGE_UNGZIP_WINDOWS_ANDROID%
    )
    if not "%PACKAGE_UNZIP_WINDOWS_ANDROID%" == "" (
       set PACKAGE_UNZIP=%PACKAGE_UNZIP_WINDOWS_ANDROID%
    )
    if not "%PACKAGE_UNBZIP_WINDOWS_ANDROID%" == "" (
       set PACKAGE_UNBZIP=%PACKAGE_UNBZIP_WINDOWS_ANDROID%
    )
    if not "%PACKAGE_UNTAR_WINDOWS_ANDROID%" == "" (
       set PACKAGE_UNTAR=%PACKAGE_UNTAR_WINDOWS_ANDROID%
    )

  ) else (

    if not "%PACKAGE_URL_WINDOWS%" == "" (
       set PACKAGE_URL=%PACKAGE_URL_WINDOWS%
    )
    if not "%PACKAGE_NAME_WINDOWS%" == "" (
       set PACKAGE_NAME=%PACKAGE_NAME_WINDOWS%
    )
    if not "%PACKAGE_UNGZIP_WINDOWS%" == "" (
       set PACKAGE_UNGZIP=%PACKAGE_UNGZIP_WINDOWS%
    )
    if not "%PACKAGE_UNZIP_WINDOWS%" == "" (
       set PACKAGE_UNZIP=%PACKAGE_UNZIP_WINDOWS%
    )
    if not "%PACKAGE_UNBZIP_WINDOWS%" == "" (
       set PACKAGE_UNBZIP=%PACKAGE_UNBZIP_WINDOWS%
    )
    if not "%PACKAGE_UNTAR_WINDOWS%" == "" (
       set PACKAGE_UNTAR=%PACKAGE_UNTAR_WINDOWS%
    )

  )
)

rem ############################################################
set PF=%PACKAGE_URL%/%PACKAGE_NAME%

if "%PACKAGE_WGET%" == "YES" (
  echo.
  echo Downloading package from '%PF%' ...
  echo.

  if EXIST "%PACKAGE_NAME%" (
    del /Q /S %PACKAGE_NAME%
  )

  if not "%PACKAGE_WGET_HEADER%" == "" (
     wget --no-check-certificate %PACKAGE_WGET_EXTRA% --header="%PACKAGE_WGET_HEADER%" "%PF%"
     rem -O%PACKAGE_NAME%
  ) else (
     wget --no-check-certificate %PACKAGE_WGET_EXTRA% "%PF%"
     rem -O%PACKAGE_NAME%
  )

  if %errorlevel% neq 0 (
   echo.
   echo Error: Failed downloading package ...
   goto err
  )

  if "%PACKAGE_RENAME%" == "YES" (
    rem Sometimes wget on Windows downloads file without extension
    rem though seems like last version fixes that. Hence next check
    if EXIST "%PACKAGE_NAME2%" (
      ren %PACKAGE_NAME2% %PACKAGE_NAME%
    )
  )
)

if "%PACKAGE_GIT%" == "YES" (
  echo.
  echo Cloning package from '%PF%' ...
  echo.

  if EXIST "%PACKAGE_SUB_DIR%" (
    rd /s /q %PACKAGE_SUB_DIR%
    ping -n 2 192.192.192.192 -w 1000 > nul
  )

  if EXIST "%PACKAGE_SUB_DIR%" (
    rd %PACKAGE_SUB_DIR%
    ping -n 2 192.192.192.192 -w 1000 > nul
  )

  git clone %PACKAGE_GIT_CLONE_FLAGS% %PACKAGE_URL% %PACKAGE_SUB_DIR%

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

    cd ..
  )

  if "%PACKAGE_GIT_SUBMODULES%" == "YES" (
    cd %PACKAGE_SUB_DIR%

    echo.
    echo Initialization git submodules ...
    echo.

    git submodule init
    git submodule update

    if %errorlevel% neq 0 (
     echo.
     echo Error: git submodule initialization failed!
     goto err
    )

    cd ..
  )
)

rem ############################################################
if "%PACKAGE_UNGZIP%" == "YES" (
  echo.
  echo Ungzipping archive ...
  echo.

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
if "%PACKAGE_UN7ZIP%" == "YES" (
  echo.
  echo Un7zipping archive ...
  echo.

  if EXIST "%PACKAGE_NAME1%" (
    del /Q /S %PACKAGE_NAME1%
  )

  7z x %PACKAGE_NAME%

  if %errorlevel% neq 0 (
   echo.
   echo Error: un7zipping package failed!
   goto err
  )
)

rem ############################################################
if "%PACKAGE_UNZIP%" == "YES" (
  echo.
  echo Unzipping archive ...
  echo.

  unzip %PACKAGE_NAME%

  if %errorlevel% neq 0 (
    if not "%PACKAGE_UNZIP_SKIP_ERROR%" == "YES" (
      echo.
      echo Error: unzipping package failed!
      goto err
    )
  )
)

rem ############################################################
if "%PACKAGE_UNBZIP%" == "YES" (
  echo.
  echo Unbzipping archive ...
  echo.

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
    rd /s /q %PACKAGE_SUB_DIR%
    ping -n 2 192.192.192.192 -w 1000 > nul
  )

  if EXIST "%PACKAGE_SUB_DIR%" (
    rd %PACKAGE_SUB_DIR%
    ping -n 2 192.192.192.192 -w 1000 > nul
  )

  tar xvf %PACKAGE_NAME1% %PACKAGE_UNTAR_EXTRA%

  if NOT "%PACKAGE_UNTAR_SKIP_ERROR_WIN%" == "YES" (
    if %errorlevel% neq 0 (
      echo.
      echo Error: untaring package failed!
      goto err
    )
  )
)

rem ############################################################
if "%PACKAGE_UNXTAR%" == "YES" (
  echo.
  echo UnXtarring archive ...

  if EXIST "%PACKAGE_SUB_DIR%" (
    rd /s /q %PACKAGE_SUB_DIR%
    ping -n 2 192.192.192.192 -w 1000 > nul
  )

  if EXIST "%PACKAGE_SUB_DIR%" (
    rd %PACKAGE_SUB_DIR%
    ping -n 2 192.192.192.192 -w 1000 > nul
  )

  tar xvfJ %PACKAGE_NAME% %PACKAGE_UNTAR_EXTRA%

  if NOT "%PACKAGE_UNTAR_SKIP_ERROR_WIN%" == "YES" (
    if %errorlevel% neq 0 (
      echo.
      echo Error: untaring package failed!
      goto err
    )
  )
)

cd /D %INSTALL_DIR%

rem ############################################################
if "%PACKAGE_RUN%" == "YES" (
  echo.
  echo Running %PACKAGE_NAME% %PACKAGE_CMD% ...
  echo.

  %PACKAGE_NAME% %PACKAGE_CMD%
)

rem ############################################################
if not "%PACKAGE_RUN_EXTRA_WINDOWS%" == "" (
  echo.
  echo Running %PACKAGE_RUN_EXTRA_WINDOWS% ...
  echo.

  %PACKAGE_RUN_EXTRA_WINDOWS%
)

rem ############################################################
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
    echo.

    xcopy /E %ORIGINAL_PACKAGE_DIR%\copy\* %INSTALL_DIR%\%PACKAGE_SUB_DIR1%
  )

  if EXIST "%ORIGINAL_PACKAGE_DIR%\copy.%CK_TARGET_OS_ID%" (
    echo.
    echo Copying extra files for %CK_TARGET_OS_ID% to source dir ...
    echo.

    xcopy /E %ORIGINAL_PACKAGE_DIR%\copy.%CK_TARGET_OS_ID%\* %INSTALL_DIR%\%PACKAGE_SUB_DIR1%
  )
)

rem ############################################################
if "%PACKAGE_PATCH%" == "YES" (
  if EXIST "%ORIGINAL_PACKAGE_DIR%\patch.%CK_TARGET_OS_ID%" (
    echo.
    echo Patching source directory ...
    echo.

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

cd /D %INSTALL_DIR%

rem ############################################################
echo.
echo Cleaning ...

if NOT "%PACKAGE_SKIP_CLEAN_INSTALL%" == "YES" (

  if EXIST install (
    rd /s /q install
    ping -n 2 192.192.192.192 -w 1000 > nul

  )
  if EXIST install (
    rd install
    ping -n 2 192.192.192.192 -w 1000 > nul
  )

)

if NOT "%PACKAGE_SKIP_CLEAN_OBJ%" == "YES" (

  if EXIST obj (
    rd /s /q obj
    ping -n 2 192.192.192.192 -w 1000 > nul
  )
  if EXIST obj (
    rd obj
    ping -n 2 192.192.192.192 -w 1000 > nul
  )

)

if NOT EXIST obj (

  md obj

rem  if %errorlevel% neq 0 (
rem    echo.
rem    echo Error: problem creating obj directory!
rem    goto err
rem  )
)

rem ############################################################
if EXIST "%ORIGINAL_PACKAGE_DIR%\scripts.%CK_TARGET_OS_ID%\install.bat" (
  echo.
  echo Executing extra script ...
  echo.

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

rem Checking RANLIB
set XCMAKE_RANLIB=
if not "%CK_RANLIB_PATH_FOR_CMAKE%" == "" (
 set XCMAKE_RANLIB=-DCMAKE_RANLIB="%CK_RANLIB_PATH_FOR_CMAKE%"
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

  if not "%PACKAGE_SKIP_CONFIGURE%" == "YES" (

     rem ############################################################
     echo.
     echo Configuring ...
     echo.

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
           %XCMAKE_RANLIB% ^
           %XCMAKE_LD% ^
           %XCMAKE_EXE_LINKER_FLAGS% ^
           %XCMAKE_EXE_LINKER_LIBS% ^
           %CK_CMAKE_EXTRA% ^
           %INSTALL_DIR%\%PACKAGE_SUB_DIR1%
  )

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

%CK_MAKE_CMD2%

rem ############################################################
if EXIST "%ORIGINAL_PACKAGE_DIR%\scripts.%CK_TARGET_OS_ID%\post-install.bat" (
  echo.
  echo Executing extra script ...
  echo.

  call %ORIGINAL_PACKAGE_DIR%\scripts.%CK_TARGET_OS_ID%\post-install.bat

  if %errorlevel% neq 0 (
   echo.
   echo Error: Failed executing extra script ...
   goto err
  )
)

rem  ############################################################
if NOT "%PACKAGE_SKIP_CLEAN_OBJ%" == "YES" (
  echo.
  echo Cleaning obj directory ...
  echo.

  if EXIST obj (
    rd /s /q obj
    ping -n 2 192.192.192.192 -w 1000 > nul
  )
  if EXIST obj (
    rd obj
    ping -n 2 192.192.192.192 -w 1000 > nul
  )
)

rem  ############################################################
rem  CAREFUL - when GIT, CK can't afterwards go to this dir to get revision number ...

rem if NOT "%PACKAGE_SKIP_CLEAN_SRC_DIR%" == "YES" (
rem  echo.
rem  echo Cleaning src directory ...
rem
rem   if EXIST src (
rem    rd /s /q src
rem  )
rem  if EXIST src (
rem    rd src
rem  )
)

exit /b 0

:err
exit /b 1
