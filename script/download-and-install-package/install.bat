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

rem set > %PACKAGE_DIR%\xyz
rem exit /b 1

rem ############################################################
set PF=%PACKAGE_URL%/%PACKAGE_NAME%

if "%PACKAGE_WGET%" == "YES" (
  echo.
  echo Downloading package from '%PF%' ...

  if EXIST %PF (
    del /Q /S %PF%
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

  if EXIST %PACKAGE_SUB_DIR% (
    rmdir /s /q %PACKAGE_SUB_DIR%
    rmdir %PACKAGE_SUB_DIR%
  )

  git clone %PACKAGE_URL% %PACKAGE_SUB_DIR%

  if %errorlevel% neq 0 (
   echo.
   echo Error: Failed cloning package ...
   goto err
  )
)

rem ############################################################
if "%PACKAGE_UNGZIP%" == "YES" (
  echo.
  echo Ungzipping archive ...

  if EXIST %PACKAGE_NAME1% (
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
if "%PACKAGE_UNTAR%" == "YES" (
  echo.
  echo Untarring archive ...

  if EXIST %PACKAGE_SUB_DIR% (
    rmdir /s /q %PACKAGE_SUB_DIR%
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

rem ############################################################
if "%PACKAGE_COPY%" == "YES" (
  if EXIST %ORIGINAL_PACKAGE_DIR%\copy (
    echo.
    echo Copying extra files to source dir ...

    xcopy /E %ORIGINAL_PACKAGE_DIR%\copy\* %INSTALL_DIR%\%PACKAGE_SUB_DIR1%
  )

  if EXIST %ORIGINAL_PACKAGE_DIR%\copy.%CK_TARGET_OS_ID% (
    echo.
    echo Copying extra files for %CK_TARGET_OS_ID% to source dir ...

    xcopy /E %ORIGINAL_PACKAGE_DIR%\copy.%CK_TARGET_OS_ID%\* %INSTALL_DIR%\%PACKAGE_SUB_DIR1%
  )
)

rem ############################################################
if "%PACKAGE_PATCH%" == "YES" (
  if EXIST %ORIGINAL_PACKAGE_DIR%\patch.%CK_TARGET_OS_ID% (
    echo.
    echo patching source dir ...

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
echo Configuring ...

cd /D %INSTALL_DIR%

if EXIST install (
  rmdir /s /q install
  rmdir install
)

if EXIST obj (
  rmdir /s /q obj
  rmdir obj
)
mkdir obj

cd /D %INSTALL_DIR%/obj

cmake -DCMAKE_INSTALL_PREFIX="%INSTALL_DIR%\install" ^
      -DCMAKE_BUILD_TYPE:STRING=%CMAKE_CONFIG% ^
      %PACKAGE_CONFIGURE_FLAGS% ^
      -DCMAKE_C_COMPILER="%CK_CC_PATH_FOR_CMAKE%" ^
      -DCMAKE_C_FLAGS="%CK_CC_FLAGS_FOR_CMAKE% %CK_CC_FLAGS_ANDROID_TYPICAL%" ^
      -DCMAKE_CXX_COMPILER="%CK_CXX_PATH_FOR_CMAKE%" ^
      -DCMAKE_CXX_FLAGS="%CK_CXX_FLAGS_FOR_CMAKE% %CK_CXX_FLAGS_ANDROID_TYPICAL%" ^
      -DCMAKE_AR="%CK_AR_PATH_FOR_CMAKE%" ^
      -DCMAKE_LINKER="%CK_LD_PATH_FOR_CMAKE%" ^
      -DCMAKE_EXE_LINKER_FLAGS="%CK_LINKER_FLAGS_ANDROID_TYPICAL%" ^
      -DCMAKE_EXE_LINKER_LIBS="%CK_LINKER_LIBS_ANDROID_TYPICAL%" ^
      %CK_CMAKE_EXTRA% ^
      %INSTALL_DIR%\%PACKAGE_SUB_DIR1%

echo **************************************************************
echo.
echo Building using Visual Studio ...

cmake --build . --config %CMAKE_CONFIG% --target install
if %errorlevel% neq 0 (
 echo.
 echo Problem building CK package!
 goto err
)

exit /b 0

:err
exit /b 1
