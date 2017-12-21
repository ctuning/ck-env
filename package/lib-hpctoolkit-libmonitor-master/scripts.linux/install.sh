#! /bin/bash

#
# Installation script for PAPI
#
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}/${PACKAGE_SUB_DIR}

export CC=gcc
export CXX=g++
export FC=gfortran
export F77=gfortran

############################################################
echo ""
echo "Configuring package ..."

./configure --prefix="${INSTALL_DIR}/install" ${PACKAGE_CONFIGURE_FLAGS}

if [ "${?}" != "0" ] ; then
  echo "Error: configure failed!"
  exit 1
fi

############################################################
echo ""
echo "Building package ..."

make ${CK_MAKE_BEFORE} -j ${CK_HOST_CPU_NUMBER_OF_PROCESSORS} ${CK_MAKE_EXTRA}
if [ "${?}" != "0" ] ; then
  echo "Error: build failed!"
  exit 1
fi

############################################################
echo ""
echo "Installing package ..."

rm -rf "${INSTALL_DIR}/install"
make install

if [ "${?}" != "0" ] ; then
  echo "Error: build failed!"
  exit 1
fi

############################################################
echo ""
echo "Building examples ..."

cd ${CK_ENV_LIB_PAPI_SRC}
rm -rf examples.new
mkdir examples.new
cd examples.new

cp ${ORIGINAL_PACKAGE_DIR}/papi_examples.tar.gz .
gunzip papi_examples.tar.gz
tar xvf papi_examples.tar

make clean
make

if [ "${?}" != "0" ] ; then
  echo "Error: build failed!"
  exit 1
fi

############################################################
echo ""
echo "Creating libPapiMonitor.so ..."
gcc -shared -g -o libPapiMonitor.so PAPI_overflow_libmonitor.o ${CK_ENV_LIB_PAPI_LIB}/libpapi.so -L${CK_ENV_LIB_PAPI_LIB} -pthread -lrt

if [ "${?}" != "0" ] ; then
  echo "Error: build failed!"
  exit 1
fi

ldd libPapiMonitor.so

############################################################
echo ""
echo "Copying libPapiMonitor.so ..."
cp libPapiMonitor.so $INSTALL_DIR/install/lib

############################################################
cd ${CK_ENV_LIB_PAPI_SRC}
cd libpfm4/perf_examples
make

if [ "${?}" != "0" ] ; then
  echo "Error: build failed!"
  exit 1
fi


return 0
