#!/bin/bash

#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#
# Developer(s):
# - Leo Gordon, 2018
# - Ivan Osipov, 2019
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

CXX=${CK_CXX} \
CC="${CK_CC} ${CK_COMPILER_FLAGS_OBLIGATORY} ${CK_CC_FLAGS_FOR_CMAKE} ${CK_CC_FLAGS_ANDROID_TYPICAL} ${EXTRA_FLAGS}" \
ndk-build \
    APP_ABI=${CK_ANDROID_ABI} \
    APP_STL=c++_static \
    APP_PLATFORM=${CK_ANDROID_NDK_PLATFORM} \
    NDK_PROJECT_PATH=. \
    APP_BUILD_SCRIPT=${FLATBUFFERS_SOURCE_DIR}/android/jni/Android.mk

rm -rf ${FLATBUFFERS_TARGET_DIR}

mkdir ${FLATBUFFERS_TARGET_DIR} ${FLATBUFFERS_TARGET_DIR}/lib ${FLATBUFFERS_TARGET_DIR}/include

cp ${FLATBUFFERS_BUILD_DIR}/obj/local/${CK_ANDROID_ABI}/*.a ${FLATBUFFERS_TARGET_DIR}/lib
cp ${FLATBUFFERS_BUILD_DIR}/obj/local/${CK_ANDROID_ABI}/*.so ${FLATBUFFERS_TARGET_DIR}/lib
cp -R ${FLATBUFFERS_SOURCE_DIR}/include/flatbuffers ${FLATBUFFERS_TARGET_DIR}/include
