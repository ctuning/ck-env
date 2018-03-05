#!/bin/bash

#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Leo Gordon, 2018
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}/leveldb-1.20


############################################################
echo ""
echo "Building package ..."

    # on a Mac and compiling with LLVM:
if [ -n "$CK_ENV_COMPILER_LLVM_SET" ] && [ "$CK_DLL_EXT" = ".dylib" ]
then
    make CXX="${CK_ENV_COMPILER_LLVM_BIN}/${CK_CXX} -stdlib=libstdc++" CC="${CK_ENV_COMPILER_LLVM_BIN}/${CK_CC}" LDFLAGS="-lstdc++"
else
    make
fi

if [ "${?}" != "0" ] ; then
  echo "Error: build failed!"
  exit 1
fi

############################################################
echo ""
echo "Installing package ..."

mkdir -p $INSTALL_DIR/install/include
cp -r $INSTALL_DIR/leveldb-1.20/include $INSTALL_DIR/install

mkdir -p $INSTALL_DIR/install/lib
cp $INSTALL_DIR/leveldb-1.20/out-static/*.a $INSTALL_DIR/install/lib
cp $INSTALL_DIR/leveldb-1.20/out-shared/*${CK_DLL_EXT} $INSTALL_DIR/install/lib

exit 0
