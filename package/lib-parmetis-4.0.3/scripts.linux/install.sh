#! /bin/bash

#
# Extra installation script
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#
# Developer(s):
# - Grigori Fursin, grigori.fursin@cTuning.org, 2017
#

cd ${INSTALL_DIR}/${PACKAGE_SUB_DIR}

PREFIX=${INSTALL_DIR}/install

make config shared=1 prefix=$PREFIX cc=${CK_ENV_LIB_MPI_CC}
if [ "${?}" != "0" ] ; then
    echo "Error: configure failed!"
      exit 1
fi



make install;
if [ "${?}" != "0" ] ; then
    echo "Error: make installation failed!"
      exit 1
fi

#make check
