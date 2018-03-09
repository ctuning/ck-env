#!/bin/bash

#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Leo Gordon, 2018
#

# for example,
#   INSTALL_DIR     = "~/CK-TOOLS/lib-leveldb-1.20-llvm-5.0.0-macos-64"
#   PACKAGE_SUB_DIR = "leveldb-1.20"

BUILD_DIR=$INSTALL_DIR/$PACKAGE_SUB_DIR
TARGET_DIR=$INSTALL_DIR/install

############################################################
echo ""
echo "Building package ${PACKAGE_SUB_DIR} in ${BUILD_DIR} ..."

cd $BUILD_DIR

    # on a Mac and compiling with LLVM:
if [ -n "$CK_ENV_COMPILER_LLVM_SET" ] && [ "$CK_DLL_EXT" = ".dylib" ]
then
    make CXX="${CK_ENV_COMPILER_LLVM_BIN}/${CK_CXX} -stdlib=libstdc++" CC="${CK_ENV_COMPILER_LLVM_BIN}/${CK_CC}" LDFLAGS="-lstdc++"
else
    # NOTE: the obvious AR=$CK_AR won't work for this Makefile, because:
    #   (1) llvm-ar refuses to take -rs argument
    #   (2) the current version of CK_AR defined by soft:compiler.llvm doesn't contain the version number
    make CXX=$CK_CXX CC=$CK_CC
fi

if [ "${?}" != "0" ] ; then
    echo "Error: build failed!"
    exit 1
fi

############################################################
echo ""
echo "Installing package ${PACKAGE_SUB_DIR} to ${TARGET_DIR} ..."

mkdir -p $TARGET_DIR/include
cp -r $BUILD_DIR/include $TARGET_DIR

mkdir -p $TARGET_DIR/lib

    # preserve local symbolic links that may help us to identify the version later:
cp -a $BUILD_DIR/out-static/*${CK_LIB_EXT}* $TARGET_DIR/lib
cp -a $BUILD_DIR/out-shared/*${CK_DLL_EXT}* $TARGET_DIR/lib

exit 0
