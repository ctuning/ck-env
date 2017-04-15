#! /bin/bash

#
# Installation script for CK packages.
#
# See CK LICENSE.txt for licensing details.
# See CK Copyright.txt for copyright details.
#
# Developer(s): Grigori Fursin, 2015
#

# PACKAGE_DIR
# INSTALL_DIR

export LIB_NAME=libOpenCL

echo ""
echo "Copying OpenCL stubs to src dir ..."
echo ""

mkdir ${INSTALL_DIR}/src
mkdir ${INSTALL_DIR}/lib
mkdir ${INSTALL_DIR}/include
mkdir ${INSTALL_DIR}/include/CL

cp ${PACKAGE_DIR}/lib/stubs.c ${INSTALL_DIR}/src
cp ${PACKAGE_DIR}/ck-make.sh ${INSTALL_DIR}/src
cp ${PACKAGE_DIR}/README ${INSTALL_DIR}
cp ${PACKAGE_DIR}/include/CL/* ${INSTALL_DIR}/include/CL

cd ${INSTALL_DIR}/src

. ./ck-make.sh
 if [ "${?}" != "0" ] ; then
  echo "Error: Compilation failed in $PWD!" 
  exit 1
 fi
