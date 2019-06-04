#!/bin/bash

#############################################
#                                           #
#   NDK standalone toolchain installation   #
#                                           #
#############################################

# PACKAGE_DIR
# INSTALL_DIR

if [ "${_ARM}" == "yes" ]
then
    ${CK_ANDROID_NDK_ROOT_DIR}/build/tools/make_standalone_toolchain.py \
        --arch arm \
        --api ${_API_VERSION} \
        --install-dir ${INSTALL_DIR}/arm
fi

if [ "${_ARM64}" == "yes" ]
then
    ${CK_ANDROID_NDK_ROOT_DIR}/build/tools/make_standalone_toolchain.py \
        --arch arm64 \
        --api ${_API_VERSION} \
        --install-dir ${INSTALL_DIR}/arm64
fi

if [ "${_MIPS}" == "yes" ]
then
    ${CK_ANDROID_NDK_ROOT_DIR}/build/tools/make_standalone_toolchain.py \
        --arch mips \
        --api ${_API_VERSION} \
        --install-dir ${INSTALL_DIR}/mips
fi

if [ "${_MIPS64}" == "yes" ]
then
    ${CK_ANDROID_NDK_ROOT_DIR}/build/tools/make_standalone_toolchain.py \
        --arch mips64 \
        --api ${_API_VERSION} \
        --install-dir ${INSTALL_DIR}/mips64
fi

if [ "${_X86}" == "yes" ]
then
    ${CK_ANDROID_NDK_ROOT_DIR}/build/tools/make_standalone_toolchain.py \
        --arch x86 \
        --api ${_API_VERSION} \
        --install-dir ${INSTALL_DIR}/x86
fi

if [ "${_X86_64}" == "yes" ]
then
    ${CK_ANDROID_NDK_ROOT_DIR}/build/tools/make_standalone_toolchain.py \
        --arch x86_64 \
        --api ${_API_VERSION} \
        --install-dir ${INSTALL_DIR}/x86_64
fi
