#! /bin/bash

#
# CK post installation script for Glow compiler.
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#

# Environment variables defined by CK:

# PACKAGE_DIR
# INSTALL_DIR

function exit_if_error() {
  message=${1:-"unknown"}
  if [ "${?}" != "0" ]; then
    echo "Error: ${message}!"
    exit 1
  fi
}


SRC_DIR=${INSTALL_DIR}/glow
BUILD_DIR=${INSTALL_DIR}/install

# Update the submodules
echo "Updating submodules ..."
cd ${SRC_DIR}
git submodule update --init --recursive


mkdir -p ${BUILD_DIR}


# Create the build and install dirs
cd ${INSTALL_DIR}

# Configure the package.
read -d '' CMK_CMD <<EO_CMK_CMD
${CK_ENV_TOOL_CMAKE_BIN}/cmake \
  -G Ninja \
  -DCMAKE_C_COMPILER="${CK_CC_PATH_FOR_CMAKE}" \
  -DCMAKE_C_FLAGS="${CK_CC_FLAGS_FOR_CMAKE} ${EXTRA_FLAGS}" \
  -DCMAKE_CXX_COMPILER="${CK_CXX_PATH_FOR_CMAKE}" \
  -DCMAKE_CXX_FLAGS="${CK_CXX_FLAGS_FOR_CMAKE} ${EXTRA_FLAGS}" \
  -DCMAKE_AR="${CK_AR_PATH_FOR_CMAKE}" \
  -DCMAKE_RANLIB="${CK_RANLIB_PATH_FOR_CMAKE}" \
  -DCMAKE_LINKER="${CK_LD_PATH_FOR_CMAKE}" \
  -DBoost_NO_BOOST_CMAKE=TRUE \
  -DBoost_NO_SYSTEM_PATHS=TRUE \
  -DBOOST_ROOT:PATHNAME=${CK_ENV_LIB_BOOST} \
  -DBoost_LIBRARY_DIRS:FILEPATH=${CK_ENV_LIB_BOOST}/lib \
  -DCMAKE_BUILD_TYPE=Release \
  -DGLOG_LIBRARY=${CK_ENV_LIB_GLOG_LIB}/libglog.so \
  -DGLOG_INCLUDE_DIR=${CK_ENV_LIB_GLOG_INCLUDE} \
  -Dfmt_DIR=${CK_ENV_LIB_FMT_OBJ_DIR} \
  -DLLVM_DIR=${CK_ENV_COMPILER_LLVM_LIB}/cmake/llvm \
  -DGLOW_BUILD_TESTS=OFF \
  -DGLOW_WITH_CPU=ON \
  -DGLOW_WITH_OPENCL=OFF \
  -DGLOW_WITH_BUNDLES=ON \
  ${CK_GLOW_EXTRA_FLAGS} \
  "${SRC_DIR}"
EO_CMK_CMD


# First, print the EXACT command we are about to run.
echo "Configuring the package with 'CMake' ..."
echo ${CMK_CMD}
echo
# Now, run it from the build directory.
cd ${BUILD_DIR} && eval ${CMK_CMD}
exit_if_error "CMake failed"


# Now, run the ninja command to build.
eval ninja all
exit_if_error "Ninja build failed"


return 0
