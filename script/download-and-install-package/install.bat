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

  del /Q /S %PF%

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

  rmdir /s /q %PACKAGE_SUB_DIR%
  rmdir %PACKAGE_SUB_DIR%

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

  del /Q /S %PACKAGE_NAME1%
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

  rmdir /s /q %PACKAGE_SUB_DIR%
  rmdir %PACKAGE_SUB_DIR%

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
echo.
echo Configuring ...

rmdir /s /q install
rmdir install

rmdir /s /q obj
rmdir obj
mkdir obj

cd /D %INSTALL_DIR%/obj

cmake -DCMAKE_INSTALL_PREFIX="%INSTALL_DIR%\install" ^
      -DCMAKE_BUILD_TYPE:STRING=%CMAKE_CONFIG% ^
      %PACKAGE_CONFIGURE_FLAGS% ^
      %PACKAGE_CONFIGURE_FLAGS_WINDOWS% ^
      -DCMAKE_C_COMPILER="%CK_CC_PATH_FOR_CMAKE%" \
      -DCMAKE_C_FLAGS="%CK_CC_FLAGS_FOR_CMAKE% %CK_CC_FLAGS_ANDROID_TYPICAL%" \
      -DCMAKE_CXX_COMPILER="%CK_CXX_PATH_FOR_CMAKE%" \
      -DCMAKE_CXX_FLAGS="%CK_CXX_FLAGS_FOR_CMAKE% %CK_CXX_FLAGS_ANDROID_TYPICAL%" \
      -DCMAKE_AR="%CK_AR_PATH_FOR_CMAKE%" \
      -DCMAKE_LINKER="%CK_LD_PATH_FOR_CMAKE%" \
      -DCMAKE_EXE_LINKER_FLAGS="%CK_LINKER_FLAGS_ANDROID_TYPICAL%" \
      -DCMAKE_EXE_LINKER_LIBS="%CK_LINKER_LIBS_ANDROID_TYPICAL%" \
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
