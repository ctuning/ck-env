#! /bin/bash

#
# Installation script for dividiti's OpenCL profiler.
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#
# Developer(s):
# - Grigori Fursin, grigori@dividiti.com, 2015
# - Anton Lokhmotov, anton@dividiti.com, 2016-2017
#

# Standard env.
# INSTALL_DIR
# PACKAGE_DIR

# Custom env (./cm/meta.json).
# PACKAGE_URL
# PACKAGE_BRANCH
# PACKAGE_NAME
# LIB_NAME

export SRC_DIR=${INSTALL_DIR}/src
export API_DIR=${INSTALL_DIR}/PythonAPI
export DST_DIR=`pwd`
export BLD_LOG=${INSTALL_DIR}/${PACKAGE_NAME}.log

################################################################################
echo ""
echo "Cloning '${PACKAGE_NAME}' from '${PACKAGE_URL}' ..."

rm -rf ${SRC_DIR}
git clone ${PACKAGE_URL} --no-checkout ${SRC_DIR}
if [ "${?}" != "0" ] ; then
  echo "Error: Cloning '${PACKAGE_NAME}' from '${PACKAGE_URL}' failed!"
  exit 1
fi

################################################################################
echo ""
echo "Checking out the '${PACKAGE_BRANCH}' branch of '${PACKAGE_NAME}' ..."

cd ${SRC_DIR}
git checkout ${PACKAGE_BRANCH}
if [ "${?}" != "0" ] ; then
  echo "Error: Checking out the '${PACKAGE_BRANCH}' branch of '${PACKAGE_NAME}' failed!"
  exit 1
fi

################################################################################
echo ""
echo "Logging into '${BLD_LOG}' ..."
rm ${BLD_LOG} && touch ${BLD_LOG}

echo "** DATE **" >> ${BLD_LOG}
date >> ${BLD_LOG}

echo "** SET **" >> ${BLD_LOG}
set >> ${BLD_LOG}

################################################################################
cd ${SRC_DIR}/PythonAPI
make
cp -r pycocotools/* ${API_DIR}

################################################################################
echo ""
echo "Installed '${TOOL_NAME}' to '${DST_DIR}'."
