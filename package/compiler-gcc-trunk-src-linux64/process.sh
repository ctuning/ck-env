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

export PACKAGE_NAME=src

#
echo ""
echo "Downloading GCC trunk from SVN ..."

cd ${INSTALL_DIR}
svn co svn://gcc.gnu.org/svn/gcc/trunk ${PACKAGE_NAME}

export INSTALL_OBJ_DIR=${INSTALL_DIR}/obj
mkdir $INSTALL_OBJ_DIR

#
echo ""
echo "Configuring ..."

if ["$LIBRARY_PATH" -eq ""]
then
 export LIBRARY_PATH=/usr/lib/x86_64-linux-gnu
else
 export LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LIBRARY_PATH
fi

cd ${INSTALL_OBJ_DIR}
../${PACKAGE_NAME}/configure --prefix=${INSTALL_DIR} \
                             --enable-languages=c,fortran,c++ \
                             --disable-multilib
#                             --with-gmp=${CK_ENV_LIB_GMP} \
#                             --with-mpfr=${CK_ENV_LIB_MPFR} \
#                             --with-mpc=${CK_ENV_LIB_MPC} \
#                             --with-cloog=${CK_ENV_LIB_CLOOG} \
#                             --enable-cloog-backend=isl \
#                             --disable-cloog-version-check \
#                             --enable-libgomp \
#                             --enable-lto \
#                             --enable-graphite \

# FGG had problems compiling PPL on recent machines with GCC 4.9.x
# Hence FGG decided to use provided one (apt-get install ppl-dev)
#                             --with-ppl=${CK_ENV_LIB_PPL} \

# FGG also had problems with x86 support on x64 machines,
# hence FGG added '--disable-multilib'

# FGG had issues with 'cannot find crti.o: No such file or directory',
# hence FGG added export LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LIBRARY_PATH 

if [ "${?}" != "0" ] ; then
  echo "Error: Configuration failed in $PWD!"
  exit 1
fi

# Build
echo ""
echo "Building ..."
echo ""
cd ${INSTALL_OBJ_DIR}
make
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
