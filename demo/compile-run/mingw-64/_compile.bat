call _clean.bat

call ck set env tags=compiler,lang-c,target-os-mingw-64 bat_file=tmp-ck-env.bat --bat_new --print && call tmp-ck-env.bat && del /Q tmp-ck-env.bat
if %errorlevel% neq 0 exit /b %errorlevel%

%CK_CC% %CK_COMPILER_FLAGS_OBLIGATORY% ctuning-rtl.c susan.c %CK_FLAGS_OUTPUT%a.exe %CK_EXTRA_LIB_M%
%CK_OBJDUMP% a.exe > a.lst
