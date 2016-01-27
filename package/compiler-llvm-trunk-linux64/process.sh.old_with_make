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

export OBJ_DIR=${INSTALL_DIR}/obj

echo ""
echo "Getting LLVM trunk from SVN"

svn co http://llvm.org/svn/llvm-project/llvm/trunk ${INSTALL_DIR}/trunk/llvm
svn co http://llvm.org/svn/llvm-project/cfe/trunk  ${INSTALL_DIR}/trunk/llvm/tools/clang
svn co http://llvm.org/svn/llvm-project/polly/trunk  ${INSTALL_DIR}/trunk/llvm/tools/polly
svn co http://llvm.org/svn/llvm-project/dragonegg/trunk  ${INSTALL_DIR}/trunk/llvm/projects/dragonegg

#svn co http://llvm.org/svn/llvm-project/lnt/trunk  ${INSTALL_DIR}/trunk/llvm/tools/lnt

echo ""
echo "Configuring ..."

mkdir $OBJ_DIR
cd $OBJ_DIR

../trunk/llvm/configure --prefix=${INSTALL_DIR}
if [ "$?" != "0" ]; then
 echo "Error: failed configuring ..."
 read -p "Press any key to continue!"
 exit $?
fi


echo ""
echo "Building ..."

make
if [ "$?" != "0" ]; then
 echo "Error: failed making ..."
 read -p "Press any key to continue!"
 exit $?
fi

echo ""
echo "Installing ..."

make install
if [ "$?" != "0" ]; then
 echo "Error: failed installing ..."
 read -p "Press any key to continue!"
 exit $?
fi
