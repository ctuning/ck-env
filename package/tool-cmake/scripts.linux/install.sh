#! /bin/bash

#
# CK installation script for cmake.
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#

# Environment variables defined by CK:

# PACKAGE_DIR
# INSTALL_DIR

function exit_if_error() {
  message=${1:-"unknown"}
  if [ "${?}" != "0" ]; then
    echo "Error: ${message}!"
    exit 1
  fi
}

SRC_DIR=${INSTALL_DIR}/${PACKAGE_NAME2_LINUX}

cd ${SRC_DIR}

env CC=${CK_CC} CXX=${CK_CXX} ./bootstrap
exit_if_error "Bootstrapping CMake failed"

make -j${CK_HOST_CPU_NUMBER_OF_PROCESSORS}
exit_if_error "Building CMake failed"

cd ${INSTALL_DIR}
ln -s ${SRC_DIR}/bin .

return 0

