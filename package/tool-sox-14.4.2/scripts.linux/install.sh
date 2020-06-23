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

${CK_ENV_COMPILER_PYTHON_FILE} setup.py install --home=../install

return 0
