@echo off

rem
rem Installation script for CK packages.
rem
rem See CK LICENSE.txt for licensing details.
rem See CK Copyright.txt for copyright details.
rem
rem Developer(s): Grigori Fursin, 2016-2017
rem

set CK_CMAKE_EXTRA=%CK_CMAKE_EXTRA% ^
 -DOPENCL_LIBRARIES:FILEPATH="%CK_ENV_LIB_OPENCL_LIB%\%CK_ENV_LIB_OPENCL_STATIC_NAME%" ^
 -DOPENCL_INCLUDE_DIRS:PATH="%CK_ENV_LIB_OPENCL_INCLUDE%" ^
 -DSAMPLES=ON

exit /b 0
