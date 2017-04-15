#! /bin/bash

#
# Installation script for LLVM.
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Grigori Fursin, 2015
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}

############################################################
# Check which file to download

MACHINE=$(uname -m)
if [ "${MACHINE}" == "armv7l" ]; then
  PACKAGE_FILE=${PACKAGE_FILE_ARMV7A}
elif [ "${MACHINE}" == "aarch64" ]; then
  PACKAGE_FILE=${PACKAGE_FILE_ARM64}
fi

URL=${PACKAGE_URL}/${PACKAGE_VERSION}/${PACKAGE_FILE}

############################################################
echo ""
echo "Downloading package from '${URL}' ..."

rm -f ${PACKAGE_FILE}
wget ${URL}
if [ "${?}" != "0" ] ; then
  echo "Error: downloading failed!"
  exit 1
fi

############################################################
echo ""
echo "Untarring and unzipping ..."

tar xvf ${PACKAGE_FILE} --strip 1
if [ "${?}" != "0" ] ; then
  echo "Error: untarring failed!"
  exit 1
fi

exit 0
