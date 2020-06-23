#! /bin/bash

#
# Installation script for Scons.
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Gavin Simpson, 2020
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}/${PACKAGE_SUB_DIR}

LDFLAGS="-L${CK_ENV_TOOL_FLAC}/lib" \
CFLAGS="-I${CK_ENV_TOOL_FLAC}/include" \
./configure --prefix="${INSTALL_DIR}/install" ${PACKAGE_CONFIGURE_FLAGS}

make
make install

return 0
