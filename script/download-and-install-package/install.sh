#! /bin/bash

#
# Universal installation script for CK
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Grigori Fursin, 2015-2017;
# - Anton Lokhmotov, 2016.
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}

############################################################
PF=${PACKAGE_URL}/${PACKAGE_NAME}

if [ "${PACKAGE_WGET}" == "YES" ] ; then
  echo ""
  echo "Downloading package from '${PF}' ..."

  if [ -f $PF ] ; then
    rm -f $PF
  fi

  wget --no-check-certificate ${PF}
  if [ "${?}" != "0" ] ; then
    echo "Error: downloading package failed!"
    exit 1
  fi
fi

if [ "${PACKAGE_GIT}" == "YES" ] ; then
  echo ""
  echo "Cloning archive ..."

  if [ -d ${PACKAGE_SUB_DIR} ] ; then
    rm -rf ${PACKAGE_SUB_DIR}
  fi

  git clone ${PACKAGE_URL} ${PACKAGE_SUB_DIR}

  if [ "${?}" != "0" ] ; then
    echo "Error: cloning failed!"
    exit 1
  fi
fi

############################################################
if [ "${PACKAGE_UNGZIP}" == "YES" ] ; then
  echo ""
  echo "Ungzipping archive ..."

  if [ -f ${PACKAGE_NAME1} ] ; then
    rm -f ${PACKAGE_NAME1}
  fi

  gzip -d ${PACKAGE_NAME}
  if [ "${?}" != "0" ] ; then
    echo "Error: ungzipping package failed!"
    exit 1
  fi
fi

############################################################
if [ "${PACKAGE_UNTAR}" == "YES" ] ; then
  echo ""
  echo "Untarring archive ..."

  if [ -d ${PACKAGE_SUB_DIR} ] ; then
    rm -rf ${PACKAGE_SUB_DIR}
  fi

  tar xvf ${PACKAGE_NAME1}
  if [ "${?}" != "0" ] ; then
    echo "Error: untaring package failed!"
    exit 1
  fi
fi

############################################################
if [ "${PACKAGE_COPY}" == "YES" ] ; then
  if [ -d ${ORIGINAL_PACKAGE_DIR}/copy ] ; then
    echo ""
    echo "Copying extra files to source dir ..."

    cp -rf ${ORIGINAL_PACKAGE_DIR}/copy/* ${INSTALL_DIR}/${PACKAGE_SUB_DIR1}
  fi

  if [ -d ${ORIGINAL_PACKAGE_DIR}/copy.${CK_TARGET_OS_ID} ] ; then
    echo ""
    echo "Copying extra files for ${CK_TARGET_OS_ID} to source dir ..."

    cp -rf ${ORIGINAL_PACKAGE_DIR}/copy.${CK_TARGET_OS_ID}/* ${INSTALL_DIR}/${PACKAGE_SUB_DIR1}
  fi
fi


############################################################
if [ "${PACKAGE_PATCH}" == "YES" ] ; then
  if [ -d ${ORIGINAL_PACKAGE_DIR}/patch.${CK_TARGET_OS_ID} ] ; then
    echo ""
    echo "patching source dir ..."

    cd ${INSTALL_DIR}/${PACKAGE_SUB_DIR}

    for i in ${ORIGINAL_PACKAGE_DIR}/patch.${CK_TARGET_OS_ID}/*
    do
      echo "$i"
      patch -p1 < $i

      if [ "${?}" != "0" ] ; then
        echo "Error: patching failed!"
        exit 1
      fi
    done
  fi
fi

############################################################
echo ""
echo "Cleaning ..."

cd ${INSTALL_DIR}

if [ -d install ] ; then
  rm -rf install
fi

if [ -d obj ] ; then
  rm -rf obj
fi

mkdir obj

if [ "${PACKAGE_SKIP_CLEAN_PACKAGE}" != "YES" ] ; then
 rm -rf ${PACKAGE_NAME1}
fi


############################################################
if [ "${PACKAGE_AUTOGEN}" == "YES" ] ; then
  echo ""
  echo "Executing autogen ..."

  cd ${INSTALL_DIR}/${PACKAGE_SUB_DIR}

  ./autogen.sh

  if [ "${?}" != "0" ] ; then
    echo "Error: configuring failed!"
    exit 1
  fi

fi

############################################################
echo ""

cd ${INSTALL_DIR}/obj

if [ "${PACKAGE_BUILD_TYPE}" == "configure" ] ; then
  echo "Executing configure ..."

  ../${PACKAGE_SUB_DIR}/configure --prefix="${INSTALL_DIR}/install" ${PACKAGE_CONFIGURE_FLAGS}

else
  echo "Executing cmake ..."

 cmake -DCMAKE_INSTALL_PREFIX="${INSTALL_DIR}/install" \
       ${PACKAGE_CONFIGURE_FLAGS} \
       -DCMAKE_C_COMPILER="${CK_CC_PATH_FOR_CMAKE}" \
       -DCMAKE_C_FLAGS="${CK_CC_FLAGS_FOR_CMAKE} ${CK_CC_FLAGS_ANDROID_TYPICAL} ${PACKAGE_FLAGS} ${PACKAGE_FLAGS_LINUX} ${PACKAGE_FLAGS_ANDROID}" \
       -DCMAKE_CXX_COMPILER="${CK_CXX_PATH_FOR_CMAKE}" \
       -DCMAKE_CXX_FLAGS="${CK_CXX_FLAGS_FOR_CMAKE} ${CK_CXX_FLAGS_ANDROID_TYPICAL} ${PACKAGE_FLAGS} ${PACKAGE_FLAGS_LINUX} ${PACKAGE_FLAGS_ANDROID}" \
       -DCMAKE_AR="${CK_AR_PATH_FOR_CMAKE}" \
       -DCMAKE_LINKER="${CK_LD_PATH_FOR_CMAKE}" \
       -DCMAKE_EXE_LINKER_FLAGS="${CK_LINKER_FLAGS_ANDROID_TYPICAL}" \
       -DCMAKE_EXE_LINKER_LIBS="${CK_LINKER_LIBS_ANDROID_TYPICAL}" \
        ${CK_CMAKE_EXTRA} \
        ../${PACKAGE_SUB_DIR1}
fi

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
echo "Installing package ..."

rm -rf install
make install

if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

############################################################
echo ""
echo "Cleaning obj directory ..."

if [ "${PACKAGE_SKIP_CLEAN_OBJ_DIR}" != "YES" ] ; then
 cd ${INSTALL_DIR}
 rm -rf obj
fi

############################################################
echo ""
echo "Cleaning src directory ..."

if [ "${PACKAGE_SKIP_CLEAN_SRC_DIR}" != "YES" ] ; then
 cd ${INSTALL_DIR}
 rm -rf ${PACKAGE_SUB_DIR}
fi

exit 0
