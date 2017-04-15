#! /bin/bash

#
# Installation script for clBLAS.
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Grigori Fursin, 2015;
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}

############################################################
URL=${PACKAGE_URL}/${PACKAGE_FILE}

echo ""
echo "Downloading from ${URL} ..."

rm -f ${PACKAGE_FILE}
wget ${URL}
if [ "${?}" != "0" ] ; then
  echo "Error: downloading failed!"
  exit 1
fi

############################################################
echo ""
echo "Ungzipping ..."

gzip -d ${PACKAGE_FILE}
if [ "${?}" != "0" ] ; then
  echo "Error: unbzipping failed!"
  exit 1
fi

############################################################
echo ""
echo "Untarring ..."

tar xvf ${PACKAGE_FILE1}
if [ "${?}" != "0" ] ; then
  echo "Error: untarring failed!"
  exit 1
fi

############################################################
echo ""
echo "Cleaning ..."

cd ${INSTALL_DIR}

rm -f ${PACKAGE_FILE1}

rm -rf obj
mkdir obj
cd obj

############################################################
echo ""
echo "Configuring ..."

export CPPFLAGS="-P"
../${PACKAGE_SRC}/configure --with-shared --enable-widec

if [ "${?}" != "0" ] ; then
  echo "Error: configuring failed!"
  exit 1
fi

############################################################
echo ""
echo "Building package ..."

make -j ${CK_HOST_CPU_NUMBER_OF_PROCESSORS}
if [ "${?}" != "0" ] ; then
  echo "Error: build failed!"
  exit 1
fi

############################################################
echo ""
echo "Installing package [sudo] ..."

sudo make install
if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

exit 0
