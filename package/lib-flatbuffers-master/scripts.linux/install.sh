#!/bin/bash

#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#
# Developer(s):
# - Leo Gordon, 2018
#

# for example,
#   INSTALL_DIR     = "lib-flatbuffers-linux-64"
#   PACKAGE_SUB_DIR = "src"

FLATBUFFERS_SOURCE_DIR=$INSTALL_DIR/$PACKAGE_SUB_DIR
FLATBUFFERS_BUILD_DIR=$INSTALL_DIR/obj
FLATBUFFERS_TARGET_DIR=$INSTALL_DIR/install

############################################################
echo ""
echo "Building FlatBuffers package in $INSTALL_DIR ..."
echo ""

############################################################
echo ""
echo "Running CMake for FlatBuffers ..."
echo ""

rm -rf "${FLATBUFFERS_BUILD_DIR}"
mkdir ${FLATBUFFERS_BUILD_DIR}
cd ${FLATBUFFERS_BUILD_DIR}

cmake ${FLATBUFFERS_SOURCE_DIR} \
    -G "Unix Makefiles" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_COMPILER="${CK_CC_PATH_FOR_CMAKE}" \
    -DCMAKE_C_FLAGS="${CK_CC_FLAGS_FOR_CMAKE} ${EXTRA_FLAGS}" \
    -DCMAKE_CXX_COMPILER="${CK_CXX_PATH_FOR_CMAKE}" \
    -DCMAKE_CXX_FLAGS="${CK_CXX_FLAGS_FOR_CMAKE} ${EXTRA_FLAGS} ${CK_CXX_COMPILER_STDLIB}" \
    -DCMAKE_AR="${CK_AR_PATH_FOR_CMAKE}" \
    -DCMAKE_RANLIB="${CK_RANLIB_PATH_FOR_CMAKE}" \
    -DCMAKE_LINKER="${CK_LD_PATH_FOR_CMAKE}" \
    -DCMAKE_INSTALL_PREFIX=${FLATBUFFERS_TARGET_DIR}

