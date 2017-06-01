#! /bin/bash

#
# Installation script.
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#
# Developer(s):
# - Grigori Fursin, grigori.fursin@cTuning.org, 2017
# - Anton Lokhmotov, anton@dividiti.com, 2017
#

export CK_CXX_FLAGS_FOR_CMAKE="${CK_CXX_FLAGS_FOR_CMAKE} -std=c++11"

export CK_CMAKE_EXTRA="${CK_CMAKE_EXTRA} \
 -DOPENCL_LIBRARIES:FILEPATH=${CK_ENV_LIB_OPENCL_LIB}/${CK_ENV_LIB_OPENCL_DYNAMIC_NAME} \
 -DOPENCL_INCLUDE_DIRS:PATH=${CK_ENV_LIB_OPENCL_INCLUDE} \
 -DSAMPLES=ON \
 -DANDROID=ON"
return 0
