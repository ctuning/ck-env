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

export PACKAGE_NAME=gmp-6.0.0
export PACKAGE_NAME1=${PACKAGE_NAME}a

cd ${INSTALL_DIR}
cp ${PACKAGE_DIR}/${PACKAGE_NAME1}.tar.bz2 .
bzip2 -d ${PACKAGE_NAME1}.tar.bz2
tar xvf ${PACKAGE_NAME1}.tar
rm ${PACKAGE_NAME1}.tar

export INSTALL_OBJ_DIR=${INSTALL_DIR}/obj
mkdir $INSTALL_OBJ_DIR

 echo ""
 cd ${INSTALL_OBJ_DIR}
 ../${PACKAGE_NAME}/configure --prefix=${INSTALL_DIR} --enable-cxx
 if [ "${?}" != "0" ] ; then
   echo "Error: Configuration failed in $PWD!"
   exit 1
 fi

 # Build
 echo ""
 echo "Building ..."
 echo ""
 cd ${INSTALL_OBJ_DIR}
 make $pj
  if [ "${?}" != "0" ] ; then
    echo "Error: Compilation failed in $PWD!" 
    exit 1
  fi

 # Install
 echo ""
 echo "Installing ..."
 echo ""

 make install
  if [ "${?}" != "0" ] ; then
    echo "Error: Compilation failed in $PWD!" 
    exit 1
  fi

