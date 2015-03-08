call ck setup soft @_setup_local.json --skip_path env_repo_uoa=ck-env env_data_uoa=local-llvm-w64 data_name="Compiler - LLVM local - Win64"
call ck setup soft @_setup_local.json --skip_path env_repo_uoa=ck-env env_data_uoa=local-llvm-w32 data_name="Compiler - LLVM local - Win32" target_os=windows-32
call ck setup soft @_setup_local.json --skip_path env_repo_uoa=ck-env env_data_uoa=local-llvm-mingw64 data_name="Compiler - LLVM local - MingW64" target_os=mingw-64
call ck setup soft @_setup_local.json --skip_path env_repo_uoa=ck-env env_data_uoa=local-llvm-mingw32 data_name="Compiler - LLVM local - MingW32" target_os=mingw-32
