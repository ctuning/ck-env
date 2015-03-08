@echo off

rem CK generated script

rem Soft UOA         = 
rem Host OS UOA      = windows-64
rem Target OS UOA    = windows-32
rem Target OS bits   = 32
rem Tool version     = local
rem Tool int version = 888888

rem Dependencies
call D:\Work1\CK\ck-repos\fgg-local-win\env\33543e6f0b414c9e\env.bat

set CK_ENV_COMPILER_LLVM=
set CK_ENV_COMPILER_LLVM_BIN=\bin
set CK_AFTER_COMPILE_TO_BC=ren *.o *
set CK_AR=lib
set CK_ASM_EXT=.s
set CK_BC_EXT=.bc
set CK_CC=clang
set CK_COMPILER_FLAGS_OBLIGATORY= -DWINDOWS
set CK_CXX=clang++ -fpermissive
set CK_DLL_EXT=.dll
set CK_EXE_EXT=.exe
set CK_F90=
set CK_F95=
set CK_FC=
set CK_FLAGS_CREATE_ASM=-S
set CK_FLAGS_CREATE_BC=-c -emit-llvm
set CK_FLAGS_CREATE_OBJ=-c
set CK_FLAGS_DLL=
set CK_FLAGS_DLL_EXTRA=-Xlinker /dll
set CK_FLAGS_OUTPUT=-o
set CK_FLAGS_STATIC_BIN=
set CK_FLAGS_STATIC_LIB=
set CK_FLAG_PREFIX_INCLUDE=-I
set CK_FLAG_PREFIX_VAR=-D
set CK_LB=lib
set CK_LB_OUTPUT=/OUT:
set CK_LD_FLAGS_EXTRA=-lm -ldl
set CK_LIB_EXT=.lib
set CK_MAKE=nmake
set CK_OBJDUMP=llvm-objdump -d
set CK_OBJ_EXT=.o
set CK_PLUGIN_FLAG=-fplugin=
set CK_PROFILER=gprof
set CM_INTERMEDIATE_OPT_TOOL=opt
set CM_INTERMEDIATE_OPT_TOOL_OUT=-o

exit /b 0
