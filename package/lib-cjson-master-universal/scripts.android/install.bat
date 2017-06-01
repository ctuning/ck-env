@echo off

rem
rem Installation script.
rem
rem See CK LICENSE.txt for licensing details.
rem See CK COPYRIGHT.txt for copyright details.
rem
rem Developer(s):
rem - Grigori Fursin, grigori@dividiti.com, 2016-2017
rem - Anton Lokhmotov, anton@dividiti.com, 2017
rem

set CK_CMAKE_EXTRA=%CK_CMAKE_EXTRA% ^
 -DOPENCL_LIBRARIES:FILEPATH="%CK_ENV_LIB_OPENCL_LIB%\%CK_ENV_LIB_OPENCL_DYNAMIC_NAME%" ^
 -DOPENCL_INCLUDE_DIRS:PATH="%CK_ENV_LIB_OPENCL_INCLUDE%" ^
 -DTUNERS=ON -DCLTUNE_ROOT:PATH="%CK_ENV_TOOL_CLTUNE%" ^
 -DSAMPLES=ON ^
 -DANDROID=ON

exit /b 0
