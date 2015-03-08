rem ck setup soft @_setup_local.json --skip_path env_repo_uoa=ck-env env_data_uoa=local-gcc-w64 data_name="Compiler - GCC local - Win64"
rem ck setup soft @_setup_local.json --skip_path env_repo_uoa=ck-env env_data_uoa=local-gcc-w32 data_name="Compiler - GCC local - Win32" target_os=windows-32
rem ck setup soft @_setup_local.json --skip_path env_repo_uoa=ck-env env_data_uoa=local-gcc-mingw64 data_name="Compiler - GCC local - MingW64" target_os=mingw-64
rem ck setup soft @_setup_local.json --skip_path env_repo_uoa=ck-env env_data_uoa=local-gcc-mingw32 data_name="Compiler - GCC local - MingW32" target_os=mingw-32
