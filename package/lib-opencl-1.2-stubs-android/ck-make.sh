#! /bin/bash

#
# Make script for CK libraries
# (depends on configured/installed compilers via CK)
#
# See CK LICENSE.txt for licensing details.
# See CK Copyright.txt for copyright details.
#
# Developer(s): Grigori Fursin, 2015
#

export CK_SOURCE_FILES="stubs.c"
export CK_OBJ_FILES=stubs${CK_OBJ_EXT}
export LIB_NAME=libOpenCL

export CK_COMPILER_FLAGS_MISC="${CK_FLAG_PREFIX_INCLUDE} ../include ${CK_COMPILER_FLAGS_MISC}"

echo ""
echo "Building dynamic library ..."
echo ""

export CK_TARGET_FILE=${LIB_NAME}${CK_DLL_EXT}
export CK_TARGET_FILE_D=${CK_TARGET_FILE}

export CK_CC_FLAGS="${CK_COMPILER_FLAGS_OBLIGATORY} ${CK_COMPILER_FLAGS_MISC} ${CK_COMPILER_FLAGS_CC_OPTS} ${CK_COMPILER_FLAGS_ARCH} ${CK_COMPILER_FLAGS_PAR}"

echo "Executing ${CK_CC} ${CK_OPT_SPEED} ${CK_FLAGS_DLL} ${CK_CC_FLAGS} ${CK_SOURCE_FILES} ${CK_FLAGS_OUTPUT}${CK_TARGET_FILE} ${CK_FLAGS_DLL_EXTRA} ${CK_LD_FLAGS_MISC} ${CK_LD_FLAGS_EXTRA}"
${CK_CC} ${CK_OPT_SPEED} ${CK_FLAGS_DLL} ${CK_CC_FLAGS} ${CK_SOURCE_FILES} ${CK_FLAGS_OUTPUT}${CK_TARGET_FILE} ${CK_FLAGS_DLL_EXTRA} ${CK_LD_FLAGS_MISC} ${CK_LD_FLAGS_EXTRA}
  if [ "${?}" != "0" ] ; then
    echo "Error: Compilation failed in $PWD!" 
    exit 1
  fi

echo ""
echo "Installing ..."
echo ""

mkdir ${INSTALL_DIR}/lib
cp -f ${CK_TARGET_FILE_D} ${INSTALL_DIR}/lib
