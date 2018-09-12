@echo off

rem
rem Installation script for Scons.
rem
rem See CK LICENSE.txt for licensing details.
rem See CK Copyright.txt for copyright details.
rem
rem Developer(s): Grigori Fursin, 2016-2018
rem

rem PACKAGE_DIR
rem INSTALL_DIR

cd /d %INSTALL_DIR%\%PACKAGE_SUB_DIR%

%CK_ENV_COMPILER_PYTHON_FILE% setup.py install --home=..\install

exit /b 0
