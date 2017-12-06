#! /bin/bash

#
# Installation script for PAPI
#
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}/${PACKAGE_SUB_DIR}

export CC=gcc
export CXX=g++
export FC=gfortran
export F77=gfortran

############################################################
echo ""
echo "Configuring package ..."

./configure --prefix="${INSTALL_DIR}/install" ${PACKAGE_CONFIGURE_FLAGS}

if [ "${?}" != "0" ] ; then
  echo "Error: configure failed!"
  exit 1
fi

############################################################
echo ""
echo "Building package ..."

make ${CK_MAKE_BEFORE} -j ${CK_HOST_CPU_NUMBER_OF_PROCESSORS} ${CK_MAKE_EXTRA}
if [ "${?}" != "0" ] ; then
  echo "Error: build failed!"
  exit 1
fi

############################################################
echo ""
echo "Installing package ..."

rm -rf "${INSTALL_DIR}/install"
make install

if [ "${?}" != "0" ] ; then
  echo "Error: build failed!"
  exit 1
fi

return 0
