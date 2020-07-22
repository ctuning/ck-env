#! /bin/bash

#
# Installation script for LLVM.
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Gavin Simpson, 2020
#

# PACKAGE_DIR
# INSTALL_DIR

cd ${INSTALL_DIR}

if [ ! -e "./llvm/" ]; then
    git clone --depth=1 -b "${PACKAGE_GIT_CHECKOUT}" ${PACKAGE_GIT_LLVM} llvm
fi
if [ ! -e "./clang/" ]; then
  git clone --depth=1 -b "${PACKAGE_GIT_CHECKOUT}" ${PACKAGE_GIT_CLANG} clang
fi

mkdir -p "build"
mkdir -p "install"

cd build
# LLVM_INSTALL_UTILS adds the utilities like FileCheck to the install
${CK_ENV_TOOL_CMAKE_BIN}/cmake \
    -G Ninja \
    -DCMAKE_INSTALL_PREFIX="${INSTALL_DIR}/install" \
    -DCMAKE_C_COMPILER="${CK_CC_PATH_FOR_CMAKE}" \
    -DCMAKE_C_FLAGS="${CK_CC_FLAGS_FOR_CMAKE} ${EXTRA_FLAGS}" \
    -DCMAKE_CXX_COMPILER="${CK_CXX_PATH_FOR_CMAKE}" \
    -DCMAKE_CXX_FLAGS="${CK_CXX_FLAGS_FOR_CMAKE} ${EXTRA_FLAGS}" \
    -DCMAKE_AR="${CK_AR_PATH_FOR_CMAKE}" \
    -DCMAKE_RANLIB="${CK_RANLIB_PATH_FOR_CMAKE}" \
    -DCMAKE_LINKER="${CK_LD_PATH_FOR_CMAKE}" \
    -DCMAKE_BUILD_TYPE=Release -DLLVM_INSTALL_UTILS=ON \
    -DLLVM_ENABLE_PROJECTS=clang -DLLVM_ENABLE_RTTI=ON \
    ../llvm/

cmake --build . --target install

# Delete build files
cd ${INSTALL_DIR}
rm -rf build

echo "Built LLVM into " "${INSTALL_DIR}/install"

