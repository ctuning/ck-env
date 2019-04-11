#! /bin/bash

#
# Installation script for pycocotools (Python API for the COCO dataset)
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#

export SRC_DIR=${INSTALL_DIR}/${PACKAGE_SUB_DIR}
export DST_DIR=${INSTALL_DIR}
export API_DIR=${DST_DIR}/pycocotools
export BLD_LOG=${INSTALL_DIR}/${PACKAGE_NAME}.log

SUPPRESS_WARNINGS="-Wno-misleading-indentation -Wno-maybe-uninitialized"

export CC=${CK_CC}
export CFLAGS="${CFLAGS} ${SUPPRESS_WARNINGS}"

################################################################################
echo ""
echo "Logging into '${BLD_LOG}' ..."
rm -f ${BLD_LOG} && touch ${BLD_LOG}

echo "** DATE **" >> ${BLD_LOG}
date >> ${BLD_LOG}

echo "** SET **" >> ${BLD_LOG}
set >> ${BLD_LOG}

################################################################################
cp ${ORIGINAL_PACKAGE_DIR}/Makefile ${SRC_DIR}/PythonAPI/
cd ${SRC_DIR}/PythonAPI
make
if [ "${?}" != "0" ] ; then
  echo "Error: make failed!"
  exit 1
fi

################################################################################
mkdir -p ${API_DIR}
cp -r pycocotools/* ${API_DIR}
if [ "${?}" != "0" ] ; then
  echo "Error: copy failed!"
  exit 1
fi

################################################################################
echo ""
echo "Installed '${TOOL_NAME}' to '${DST_DIR}'."
