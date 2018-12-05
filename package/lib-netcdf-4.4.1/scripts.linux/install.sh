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

export CC=${CK_ENV_LIB_MPI_CC}
export CPPFLAGS="-I${CK_ENV_LIB_HDF5_INCLUDE}"
export LDFLAGS="-L${CK_ENV_LIB_HDF5_LIB}"
PREFIX=${INSTALL_DIR}/install

echo $CPPFLAGS
echo $LDFLAGS
./configure --enable-shared=no --prefix=$PREFIX
if [ "${?}" != "0" ] ; then
    echo "Error: configure failed!"
      exit 1
fi

make
if [ "${?}" != "0" ] ; then
    echo "Error: make failed!"
      exit 1
fi

make install;
if [ "${?}" != "0" ] ; then
    echo "Error: make installation failed!"
      exit 1
fi

#make check
