#! /bin/bash

#
# Installation script
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Grigori Fursin, 2015;
#

# PACKAGE_DIR
# INSTALL_DIR

export CC=${CK_ENV_LIB_MPI_CC}
VERSION_FC=`python "$(dirname "${BASH_SOURCE[0]}")"/check.py`
export FC=${CK_ENV_LIB_MPI_BIN}/mpif90.${VERSION_FC}
return 0
