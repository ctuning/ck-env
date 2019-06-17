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
#	_WHICH_STL		("" by default, but can also be "gnustl", "libc++" or "stlport")

STL_OPT=""
if [ -n "$_WHICH_STL" ]; then
	STL_OPT="--stl ${_WHICH_STL}"
fi

${CK_ENV_COMPILER_PYTHON_FILE} ${CK_ANDROID_NDK_ROOT_DIR}/build/tools/make_standalone_toolchain.py ${STL_OPT} \
    --arch ${_TARGET_ARCH} \
    --api ${_API_LEVEL} \
    --install-dir ${INSTALL_DIR}/install

