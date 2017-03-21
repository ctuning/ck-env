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
if [ -f "${ORIGINAL_PACKAGE_DIR}/scripts.${CK_TARGET_OS_ID}/pre-download.sh" ] ; then
  echo ""
  echo "Executing pre-download script ..."

  . ${ORIGINAL_PACKAGE_DIR}/scripts.${CK_TARGET_OS_ID}/pre-download.sh

  if [ "${?}" != "0" ] ; then
    echo "Error: Failed executing pre-download script ..."
    exit 1
  fi
fi

############################################################
# Detect proper names
if [ "$PACKAGE_DETECT_VARS" == "YES" ] ; then
  if [ "$CK_TARGET_OS_ID" == "android" ] ; then
     if [[ "$OSTYPE" == "darwin"* ]]; then
        if [ "$PACKAGE_URL_MACOS_ANDROID" != "" ] ; then
           PACKAGE_URL=$PACKAGE_URL_MACOS_ANDROID
        fi
        if [ "$PACKAGE_NAME_MACOS_ANDROID" != "" ] ; then
           PACKAGE_NAME=$PACKAGE_NAME_MACOS_ANDROID
        fi
        if [ "$PACKAGE_NAME1_MACOS_ANDROID" != "" ] ; then
           PACKAGE_NAME1=$PACKAGE_NAME1_MACOS_ANDROID
        fi
        if [ "$PACKAGE_UNGZIP_MACOS_ANDROID" != "" ] ; then
           PACKAGE_UNGZIP=$PACKAGE_UNGZIP_MACOS_ANDROID
        fi
        if [ "$PACKAGE_UNZIP_MACOS_ANDROID" != "" ] ; then
           PACKAGE_UNZIP=$PACKAGE_UNZIP_MACOS_ANDROID
        fi
        if [ "$PACKAGE_UNBZIP_MACOS_ANDROID" != "" ] ; then
           PACKAGE_UNBZIP=$PACKAGE_UNBZIP_MACOS_ANDROID
        fi
        if [ "$PACKAGE_UNTAR_MACOS_ANDROID" != "" ] ; then
           PACKAGE_UNTAR=$PACKAGE_UNTAR_MACOS_ANDROID
        fi
     else
        if [ "$PACKAGE_URL_LINUX_ANDROID" != "" ] ; then
           PACKAGE_URL=$PACKAGE_URL_LINUX_ANDROID
        fi
        if [ "$PACKAGE_NAME_LINUX_ANDROID" != "" ] ; then
           PACKAGE_NAME=$PACKAGE_NAME_LINUX_ANDROID
        fi
        if [ "$PACKAGE_NAME1_LINUX_ANDROID" != "" ] ; then
           PACKAGE_NAME1=$PACKAGE_NAME1_LINUX_ANDROID
        fi
        if [ "$PACKAGE_UNGZIP_LINUX_ANDROID" != "" ] ; then
           PACKAGE_UNGZIP=$PACKAGE_UNGZIP_LINUX_ANDROID
        fi
        if [ "$PACKAGE_UNZIP_LINUX_ANDROID" != "" ] ; then
           PACKAGE_UNZIP=$PACKAGE_UNZIP_LINUX_ANDROID
        fi
        if [ "$PACKAGE_UNBZIP_LINUX_ANDROID" != "" ] ; then
           PACKAGE_UNBZIP=$PACKAGE_UNBZIP_LINUX_ANDROID
        fi
        if [ "$PACKAGE_UNTAR_LINUX_ANDROID" != "" ] ; then
           PACKAGE_UNTAR=$PACKAGE_UNTAR_LINUX_ANDROID
        fi
     fi

  else

     if [[ "$OSTYPE" == "darwin"* ]]; then
        if [ "$PACKAGE_URL_MACOS" != "" ] ; then
           PACKAGE_URL=$PACKAGE_URL_MACOS
        fi
        if [ "$PACKAGE_NAME_MACOS" != "" ] ; then
           PACKAGE_NAME=$PACKAGE_NAME_MACOS
        fi
        if [ "$PACKAGE_NAME1_MACOS" != "" ] ; then
           PACKAGE_NAME1=$PACKAGE_NAME1_MACOS
        fi
        if [ "$PACKAGE_UNGZIP_MACOS" != "" ] ; then
           PACKAGE_UNGZIP=$PACKAGE_UNGZIP_MACOS
        fi
        if [ "$PACKAGE_UNZIP_MACOS" != "" ] ; then
           PACKAGE_UNZIP=$PACKAGE_UNZIP_MACOS
        fi
        if [ "$PACKAGE_UNBZIP_MACOS" != "" ] ; then
           PACKAGE_UNBZIP=$PACKAGE_UNBZIP_MACOS
        fi
        if [ "$PACKAGE_UNTAR_MACOS" != "" ] ; then
           PACKAGE_UNTAR=$PACKAGE_UNTAR_MACOS
        fi
     else
        if [ "$PACKAGE_URL_LINUX" != "" ] ; then
           PACKAGE_URL=$PACKAGE_URL_LINUX
        fi
        if [ "$PACKAGE_NAME_LINUX" != "" ] ; then
           PACKAGE_NAME=$PACKAGE_NAME_LINUX
        fi
        if [ "$PACKAGE_NAME1_LINUX" != "" ] ; then
           PACKAGE_NAME1=$PACKAGE_NAME1_LINUX
        fi
        if [ "$PACKAGE_UNGZIP_LINUX" != "" ] ; then
           PACKAGE_UNGZIP=$PACKAGE_UNGZIP_LINUX
        fi
        if [ "$PACKAGE_UNZIP_LINUX" != "" ] ; then
           PACKAGE_UNZIP=$PACKAGE_UNZIP_LINUX
        fi
        if [ "$PACKAGE_UNBZIP_LINUX" != "" ] ; then
           PACKAGE_UNBZIP=$PACKAGE_UNBZIP_LINUX
        fi
        if [ "$PACKAGE_UNTAR_LINUX" != "" ] ; then
           PACKAGE_UNTAR=$PACKAGE_UNTAR_LINUX
        fi
     fi

  fi
fi

############################################################
PF=${PACKAGE_URL}/${PACKAGE_NAME}

if [ "${PACKAGE_WGET}" == "YES" ] ; then
  echo ""
  echo "Downloading package from '${PF}' ..."

  if [ -f ${PACKAGE_NAME} ] ; then
    rm -f ${PACKAGE_NAME}
  fi

  wget --no-check-certificate ${PF}
  if [ "${?}" != "0" ] ; then
    echo "Error: downloading package failed!"
    exit 1
  fi
fi

if [ "${PACKAGE_GIT}" == "YES" ] ; then
  echo ""
  echo "Cloning package from ${PF} ..."

  if [ -d ${PACKAGE_SUB_DIR} ] ; then
    rm -rf ${PACKAGE_SUB_DIR}
  fi

  git clone ${PACKAGE_URL} ${PACKAGE_SUB_DIR}

  if [ "${?}" != "0" ] ; then
    echo "Error: git cloning failed!"
    exit 1
  fi

  if [ "${PACKAGE_GIT_CHECKOUT}" != "" ] ; then
    cd ${PACKAGE_SUB_DIR}

    echo ""
    echo "Checking out branch ${PACKAGE_GIT_CHECKOUT} ..."
    echo ""

    git checkout ${PACKAGE_GIT_CHECKOUT}

    if [ "${?}" != "0" ] ; then
      echo "Error: git checkout failed!"
      exit 1
    fi
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
if [ "${PACKAGE_UNZIP}" == "YES" ] ; then
  echo ""
  echo "Unzipping archive ..."

  unzip ${PACKAGE_NAME}
  if [ "${?}" != "0" ] ; then
    echo "Error: unzipping package failed!"
    exit 1
  fi
fi

############################################################
if [ "${PACKAGE_UNBZIP}" == "YES" ] ; then
  echo ""
  echo "Unbzipping archive ..."

  if [ -f ${PACKAGE_NAME1} ] ; then
    rm -f ${PACKAGE_NAME1}
  fi

  echo $PACKAGE_NAME

  bzip2 -d ${PACKAGE_NAME}
  if [ "${?}" != "0" ] ; then
    echo "Error: unbzipping package failed!"
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

if [ "${PACKAGE_SKIP_CLEAN_PACKAGE}" != "YES" ] ; then
 if [ -f ${PACKAGE_NAME} ] ; then
   rm -f ${PACKAGE_NAME}
 fi
 if [ -f ${PACKAGE_NAME1} ] ; then
   rm -f ${PACKAGE_NAME1}
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
    echo "Patching source directory ..."

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

if [ "${PACKAGE_SKIP_CLEAN_INSTALL}" != "YES" ] ; then
  if [ -d install ] ; then
    rm -rf install
  fi
fi

if [ "${PACKAGE_SKIP_CLEAN_OBJ}" != "YES" ] ; then
  if [ -d obj ] ; then
    rm -rf obj
  fi
fi

if [ ! -d obj ] ; then
  mkdir obj
fi

############################################################
if [ -f "${ORIGINAL_PACKAGE_DIR}/scripts.${CK_TARGET_OS_ID}/install.sh" ] ; then
  echo ""
  echo "Executing extra script ..."

  . ${ORIGINAL_PACKAGE_DIR}/scripts.${CK_TARGET_OS_ID}/install.sh

  if [ "${?}" != "0" ] ; then
    echo "Error: Failed executing extra script ..."
    exit 1
  fi
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

elif [ "${PACKAGE_BUILD_TYPE}" == "cmake" ] ; then

  echo ""
  echo "CMake configure flags:"
  echo ""
  echo "${PACKAGE_CONFIGURE_FLAGS} ${CK_CMAKE_EXTRA}"
  echo ""

  echo "Executing cmake ..."

  XCMAKE_AR=""
  if [ "${CK_AR_PATH_FOR_CMAKE}" != "" ] ; then
    XCMAKE_AR=" -DCMAKE_AR=${CK_AR_PATH_FOR_CMAKE} "
  fi

  XCMAKE_LD=""
  if [ "${CK_LD_PATH_FOR_CMAKE}" != "" ] ; then
    XCMAKE_LD=" -DCMAKE_LINKER=${CK_LD_PATH_FOR_CMAKE} "
  fi

  cmake -DCMAKE_INSTALL_PREFIX="${INSTALL_DIR}/install" \
        ${PACKAGE_CONFIGURE_FLAGS} \
        -DCMAKE_C_COMPILER="${CK_CC_PATH_FOR_CMAKE}" \
        -DCMAKE_C_FLAGS="${CK_CC_FLAGS_FOR_CMAKE} ${CK_CC_FLAGS_ANDROID_TYPICAL} ${PACKAGE_FLAGS} ${PACKAGE_FLAGS_LINUX} ${PACKAGE_FLAGS_ANDROID}" \
        -DCMAKE_CXX_COMPILER="${CK_CXX_PATH_FOR_CMAKE}" \
        -DCMAKE_CXX_FLAGS="${CK_CXX_FLAGS_FOR_CMAKE} ${CK_CXX_FLAGS_ANDROID_TYPICAL} ${PACKAGE_FLAGS} ${PACKAGE_FLAGS_LINUX} ${PACKAGE_FLAGS_ANDROID}" \
        ${XCMAKE_AR} \
        ${XCMAKE_LD} \
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
if [ -f "${ORIGINAL_PACKAGE_DIR}/scripts.${CK_TARGET_OS_ID}/post-install.sh" ] ; then
  echo ""
  echo "Executing post-install script ..."

  . ${ORIGINAL_PACKAGE_DIR}/scripts.${CK_TARGET_OS_ID}/post-install.sh

  if [ "${?}" != "0" ] ; then
    echo "Error: Failed executing post-install script ..."
    exit 1
  fi
fi

if [ "${PACKAGE_SKIP_LINUX_MAKE}" != "YES" ] ; then 

  ############################################################
  echo ""
  echo "Building package ..."
  make -j ${CK_HOST_CPU_NUMBER_OF_PROCESSORS} ${CK_MAKE_EXTRA}
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

fi

############################################################
if [ -f "${ORIGINAL_PACKAGE_DIR}/scripts.${CK_TARGET_OS_ID}/post-install2.sh" ] ; then
  echo ""
  echo "Executing post-install2 script ..."

  . ${ORIGINAL_PACKAGE_DIR}/scripts.${CK_TARGET_OS_ID}/post-install2.sh

  if [ "${?}" != "0" ] ; then
    echo "Error: Failed executing post-install2 script ..."
    exit 1
  fi
fi


############################################################
if [ "${PACKAGE_SKIP_CLEAN_OBJ}" != "YES" ] ; then
  echo ""
  echo "Cleaning obj directory ..."

 cd ${INSTALL_DIR}
 rm -rf obj
fi

############################################################
# CAREFUL - when GIT, CK can't afterwards go to this dir to get revision number ...
#if [ "${PACKAGE_SKIP_CLEAN_SRC_DIR}" != "YES" ] ; then
# echo ""
# echo "Cleaning src directory ..."
#
# cd ${INSTALL_DIR}
# rm -rf ${PACKAGE_SUB_DIR}
#fi

exit 0
