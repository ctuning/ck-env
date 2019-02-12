#! /bin/bash

#
# Installation script for Deep500
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Grigori Fursin, 2016-2018
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}

# Clean install
if [ -d "${PACKAGE_WORK_DIR}" ]; then
  echo ""
  echo "Cleaning ${INSTALL_DIR}/${PACKAGE_WORK_DIR} directory ..."
  echo ""
  rm -rf ${PACKAGE_WORK_DIR}
fi

# Clone package

echo ""
echo "Clone package from ${PACKAGE_URL}"
echo ""
git clone ${PACKAGE_URL}

if [ "${?}" != "0" ] ; then
  echo "Error: cloning failed!"
  exit 1
fi

exit 0
