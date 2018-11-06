#! /bin/bash

#
# Installation script for Bazel on (AArch64) Linux platforms.
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#
# Developer(s):
# - Anton Lokhmotov, 2017.
#

#
# NB: Implicit dependencies (not yet in metadata):
# - Java SDK (but detected via soft description?)
# - C++ compiler
#

# PACKAGE_DIR
# INSTALL_DIR

export BAZEL_SRC_DIR=${INSTALL_DIR}/src
export BAZEL_TMP_DIR=/tmp

################################################################################
export BAZEL_INSTALL_LOG=${INSTALL_DIR}/ck-install.log

echo
echo "Logging into '${BAZEL_INSTALL_LOG}' ..."

echo "** DATE **" >> ${BAZEL_INSTALL_LOG}
date >> ${BAZEL_INSTALL_LOG}

echo "** SET **" >> ${BAZEL_INSTALL_LOG}
set >> ${BAZEL_INSTALL_LOG}

################################################################################
echo ""
echo "Downloading Bazel from '${BAZEL_URL}' ..."

echo "** WGET **" >> ${BAZEL_INSTALL_LOG}
cd ${BAZEL_TMP_DIR}
wget ${BAZEL_URL} -O ${BAZEL_ZIP} --no-check-certificate \
  >> ${BAZEL_INSTALL_LOG} 2>&1

if [ "${?}" != "0" ] ; then
  echo "Error: Downloading Bazel from '${BAZEL_URL}' failed!"
  exit 1
fi

################################################################################
echo ""
echo "Unpacking Bazel to '${BAZEL_SRC_DIR}' ..."

echo "** UNZIP **" >> ${BAZEL_INSTALL_LOG}
rm -rf ${BAZEL_SRC_DIR}
mkdir ${BAZEL_SRC_DIR}
unzip ${BAZEL_ZIP} -d ${BAZEL_SRC_DIR} \
  >> ${BAZEL_INSTALL_LOG} 2>&1

if [ "${?}" != "0" ] ; then
  echo "Error: Unpacking Bazel to '${BAZEL_SRC_DIR}' failed!"
  exit 1
fi

rm ${BAZEL_ZIP}

#################################################################################
export MACH=$(uname -m)

echo
echo "Patching Bazel ..."

echo "** PATCH **" >> ${BAZEL_INSTALL_LOG}
# Apply patch for arm machine to prevent javac running out of heap memory.
if [ "${HOSTTYPE}"  == "arm" ] ; then
  echo "Applying patch '${BAZEL_PATCH1}' ..."
  cd ${BAZEL_SRC_DIR} && patch -p1 < ${PACKAGE_DIR}/${BAZEL_PATCH1} >> ${BAZEL_INSTALL_LOG} 2>&1
fi

# Apply patch for 32-bit OS to convert error to warning in mapped_file.h.
if [ ${CK_TARGET_CPU_BITS} == 32 ]; then
  echo "Applying patch '${BAZEL_PATCH2}' ..."
  cd ${BAZEL_SRC_DIR} && patch -p1 < ${PACKAGE_DIR}/${BAZEL_PATCH2} >> ${BAZEL_INSTALL_LOG} 2>&1
fi

if [ "${?}" != "0" ] ; then
  echo "Error: Patching Bazel failed!"
  exit 1
fi

################################################################################
echo ""
echo "Compiling Bazel ..."

echo "** COMPILE **" >> ${BAZEL_INSTALL_LOG}
cd ${BAZEL_SRC_DIR}

if [ "$CK_SHOW_BAZEL_OUTPUT" == "yes" ] || [ "$CK_SHOW_BAZEL_OUTPUT" == "YES" ] ; then
  ./compile.sh
else
  ./compile.sh >> ${BAZEL_INSTALL_LOG} 2>&1
fi

if [ "${?}" != "0" ] ; then
  echo "Error: Compiling Bazel failed!"
  exit 1
fi

################################################################################
echo ""
echo "Installing Bazel ..."

echo "** INSTALL **" >> ${BAZEL_INSTALL_LOG}
mkdir -p ${INSTALL_DIR}/install
mkdir -p ${INSTALL_DIR}/install/bin
cp ${BAZEL_SRC_DIR}/output/bazel ${INSTALL_DIR}/install/bin/ >> ${BAZEL_INSTALL_LOG} 2>&1

if [ "${?}" != "0" ] ; then
  echo "Error: Installing Bazel failed!"
  exit 1
fi

###############################################################################
echo ""
echo "Successfully installed Bazel into '${INSTALL_DIR}'."
echo
