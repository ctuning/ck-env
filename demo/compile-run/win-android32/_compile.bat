call _clean.bat

call ck set env tags=compiler,lang-c,target-os-android5-arm bat_file=tmp-ck-env.bat --bat_new --print && call tmp-ck-env.bat && del /Q tmp-ck-env.bat
if %errorlevel% neq 0 exit /b %errorlevel%

%CK_CC% %CK_COMPILER_FLAGS_OBLIGATORY% ctuning-rtl.c susan.c %CK_FLAGS_OUTPUT%a.out %CK_LD_FLAGS_EXTRA% -lm
%CK_OBJDUMP% a.out > a.lst
