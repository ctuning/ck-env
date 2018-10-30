#! /bin/bash

#
# Installation script for pycocotools (Python API for COCO-dataset)
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
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
export DST_DIR=`pwd`
export API_DIR=${DST_DIR}/pycocotools
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
if [ ! -d "${API_DIR}" ]; then
  mkdir ${API_DIR}
fi
cp -r pycocotools/* ${API_DIR}

################################################################################
echo ""
echo "Installed '${TOOL_NAME}' to '${DST_DIR}'."
