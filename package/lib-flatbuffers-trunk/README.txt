# This package can be built in 4 different modes:

ck install package:lib-armnn

ck install package:lib-armnn --env.USE_NEON=1 --extra_tags=vneon --extra_version=-neon

ck install package:lib-armnn --env.USE_OPENCL=1 --extra_tags=vopencl --extra_version=-opencl

ck install package:lib-armnn --env.USE_NEON=1 --env.USE_OPENCL=1 --extra_tags=vneon,vopencl --extra_version=-neon-opencl


# NB! The order of builds is important - otherwise CK will try to reuse environments, which will screw them up.

