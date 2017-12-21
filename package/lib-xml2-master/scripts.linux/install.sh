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

cd ${INSTALL_DIR}/src

./autogen.sh --prefix=${INSTALL_DIR}/install  --with-python-install-dir=${INSTALL_DIR}/install/python-libs

return 0
