call _clean.bat

call ck set env tags=compiler,lang-c,target-os-android5-arm bat_file=tmp-ck-env.bat --bat_new --print && call tmp-ck-env.bat && del /Q tmp-ck-env.bat
if %errorlevel% neq 0 exit /b %errorlevel%

call ck set env tags=lib,mali,opencl,target-os-android5-arm bat_file=tmp-ck-env.bat --bat_new --print && call tmp-ck-env.bat && del /Q tmp-ck-env.bat
if %errorlevel% neq 0 exit /b %errorlevel%

rem echo.
rem echo %CK_CC% %CK_COMPILER_FLAGS_OBLIGATORY% -I"D:\!FGG\Installations\Mali OpenCL SDK v1.1.0\include" print_opencl_devices.c %CK_FLAGS_OUTPUT%a.out %CK_LD_FLAGS_EXTRA% -L. -lOpenCL 
rem echo.

%CK_CC% %CK_COMPILER_FLAGS_OBLIGATORY% -I"%CK_ENV_LIB_OPENCL_INCLUDE%" print_opencl_devices.c %CK_FLAGS_OUTPUT%a.out -L. -L"%CK_ENV_LIB_OPENCL_LIB%" -lOpenCL
