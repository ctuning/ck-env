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
cd ${INSTALL_DIR}/src/
PREFIX=${INSTALL_DIR}/install
mkdir -p $PREFIX
#generator requires different instructions
#make CC=gcc PREFIX=${PREFIX}
make generator CC=${CK_CC}
#fixme GET STATIC OPTION via CK ENV
make CC=${CK_CC} PREFIX=${PREFIX} STATIC=0 install
if [ "${?}" != "0" ] ; then
    echo "Error: compilation failed!"
      exit 1
fi
cp -r ${INSTALL_DIR}/src/bin ${PREFIX}
