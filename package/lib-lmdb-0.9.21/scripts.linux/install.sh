#!/bin/bash

#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Grigori Fursin, 2015;
# - Anton Lokhmotov, 2016.
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}/src/libraries/liblmdb


############################################################
echo ""
echo "Building package ..."

make -j${CK_HOST_CPU_NUMBER_OF_PROCESSORS} CC="${CK_CC} ${CK_COMPILER_FLAGS_OBLIGATORY}" AR="${CK_AR}" XCFLAGS="-DMDB_DSYNC=O_SYNC -DMDB_USE_ROBUST=0"
if [ "${?}" != "0" ] ; then
  echo "Error: build failed!"
  exit 1
fi

############################################################
echo ""
echo "Installing package ..."

make prefix="${INSTALL_DIR}/install" install
if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

exit 0
