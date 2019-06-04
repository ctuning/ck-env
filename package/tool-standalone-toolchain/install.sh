#!/bin/bash

#############################################
#                                           #
#   NDK standalone toolchain installation   #
#                                           #
#############################################

# PACKAGE_DIR
# INSTALL_DIR
#
# internal variables defined by variations:
#
#   _TARGET_ARCH    ("arm64" by default)
#   _API_LEVEL      ("24" by default -- corresponds to Android 7.0)

${CK_ANDROID_NDK_ROOT_DIR}/build/tools/make_standalone_toolchain.py \
    --arch ${_TARGET_ARCH} \
    --api ${_API_LEVEL} \
    --install-dir ${INSTALL_DIR}/install

