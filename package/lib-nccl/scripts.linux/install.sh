#! /bin/bash

#
# Extra installation script
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#
# Developer(s):
# - Grigori Fursin, grigori.fursin@cTuning.org, 2017
# - Flavio Vella, flavio@dividiti.com, 2018
# - Anton Lokhmotov, anton@dividiti.com, 2018
#

cd ${INSTALL_DIR}/${PACKAGE_SUB_DIR}

#make config shared=1 prefix=$PREFIX cc=${CK_ENV_LIB_MPI_CC}

echo "Making..."
make -j ${CK_HOST_CPU_NUMBER_OF_PROCESSORS} CXX=${CK_CXX} CUDA_HOME=${CUDA_HOME}
if [ "${?}" != "0" ] ; then
  echo "Error: making failed!"
  exit 1
fi

echo "Installing to '${PREFIX}'..."
export PREFIX=${INSTALL_DIR}/install
make install
if [ "${?}" != "0" ] ; then
  echo "Error: installing failed!"
  exit 1
fi

#make check
