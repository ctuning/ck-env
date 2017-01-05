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

echo.
echo CMake configure flags:
echo.
echo %PACKAGE_CONFIGURE_FLAGS% %CK_CMAKE_EXTRA%
echo.

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

  mkdir obj

  if %errorlevel% neq 0 (
    echo.
    echo Error: problem creating obj directory!
    goto err
  )

)

cd /D %INSTALL_DIR%/obj

if "%PACKAGE_BUILD_TYPE%" == "cmake" (

   rem ############################################################
   echo.
   echo Configuring ...

   set XCMAKE_AR=
   if not "%CK_AR_PATH_FOR_CMAKE%" == "" (
     set XCMAKE_AR=-DCMAKE_AR="%CK_AR_PATH_FOR_CMAKE%"
   )

   set XCMAKE_LD=
   if not "%CK_LD_PATH_FOR_CMAKE%" == "" (
     set XCMAKE_LD=-DCMAKE_LINKER="%CK_LD_PATH_FOR_CMAKE%"
   )

   cmake -DCMAKE_INSTALL_PREFIX="%INSTALL_DIR%\install" ^
         -DCMAKE_BUILD_TYPE:STRING=%CMAKE_CONFIG% ^
         %PACKAGE_CONFIGURE_FLAGS% ^
         -DCMAKE_C_COMPILER="%CK_CC_PATH_FOR_CMAKE%" ^
         -DCMAKE_C_FLAGS="%CK_CC_FLAGS_FOR_CMAKE% %CK_CC_FLAGS_ANDROID_TYPICAL%" ^
         -DCMAKE_CXX_COMPILER="%CK_CXX_PATH_FOR_CMAKE%" ^
         -DCMAKE_CXX_FLAGS="%CK_CXX_FLAGS_FOR_CMAKE% %CK_CXX_FLAGS_ANDROID_TYPICAL%" ^
         -DCMAKE_AR="%CK_AR_PATH_FOR_CMAKE%" ^
         -DCMAKE_LINKER="%CK_LD_PATH_FOR_CMAKE%" ^
         %XCMAKE_AR% ^
         %XCMAKE_LD% ^
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

)

exit /b 0

:err
exit /b 1
