#! /bin/bash

#
# Extra installation script
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#
# Developer(s):
# - Grigori Fursin, grigori.fursin@cTuning.org, 2017
#

export CK_CXX_FLAGS_FOR_CMAKE="${CK_CXX_FLAGS_FOR_CMAKE} -std=c++11"

export CK_CMAKE_EXTRA="${CK_CMAKE_EXTRA} \
  -DENABLE_CJSON_TEST=On \
  -DENABLE_CJSON_UTILS=On \
  -DENABLE_TARGET_EXPORT=On \
  -DENABLE_CUSTOM_COMPILER_FLAGS=On \
  -DENABLE_VALGRIND=Off \
  -DENABLE_SANITIZERS=Off \
  -DBUILD_SHARED_LIBS=On \
  -DSAMPLES=ON"

return 0
