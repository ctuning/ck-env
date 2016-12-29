#!/usr/bin/python

#
# Preparing CK compiler env for CMake
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os
import sys
import json

##############################################################################
# customize installation

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet

              path             - path to entry (with scripts)
              install_path     - installation path
            }

    Output: {
              return        - return code =  0, if successful
                                          >  0, if error
              (error)       - error text if return > 0
              (install-env) - prepare environment to be used before the install script
            }

    """

    # Get variables
    ck=i['ck_kernel']
    s=''

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    # Check platform
    hplat=hosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    phosd=hosd.get('ck_name','')

    sv1='$('
    sv2=')'

    ie={}

    svarb=hosd.get('env_var_start','')
    svarb1=hosd.get('env_var_extra1','')
    svare=hosd.get('env_var_stop','')
    svare1=hosd.get('env_var_extra2','')

    iv=i.get('interactive','')
    cus=i.get('customize',{})
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})

    # Set default parameters from compiler deps
    cd=deps['compiler']

    cdd=cd['dict']
    ce=cdd['env']
    cep=cdd['customize']['env_prefix']

    ck_cc=ce['CK_CC']
    ck_cxx=ce['CK_CXX']

    if 'clang' in ck_cc:
       ie['CK_CLANG']='YES'

    # Check if uses sub-deps GCC NDK
    ge=cdd.get('deps',{}).get('ndk-gcc',{}).get('dict',{}).get('env',{})

    # Remove flags from CK_CC
    ck_cc1=ck_cc
    ck_cc2=''
    j=ck_cc.find(' ')
    if j>0:
        ck_cc1=ck_cc[:j].strip(' "')
        ck_cc2=ck_cc[j+1:].strip(' "')

    # Remove flags from ck_cxx
    ck_cxx1=ck_cxx
    ck_cxx2=''
    j=ck_cxx.find(' ')
    if j>0:
        ck_cxx1=ck_cxx[:j].strip(' "')
        ck_cxx2=ck_cxx[j+1:].strip(' "')

    # Check that path exists
    pb=ce.get(cep,'')
    pb_cc=os.path.join(pb,'bin',ck_cc1)
    pb_cxx=os.path.join(pb,'bin',ck_cxx1)

    if not os.path.isfile(pb_cc):
        return {'return':1, 'error':'can\'t find full path to compiler ('+pb_cc+') - can\'t be used with this CMake-based package'}

    if not os.path.isfile(pb_cxx):
        return {'return':1, 'error':'can\'t find full path to compiler ('+pb_cxx+') - can\'t be used with this CMake-based package'}

    # Check AR
    pr=ce.get('CK_ANDROID_COMPILER_PREFIX','')
    if pr=='': pr=ge.get('CK_ANDROID_COMPILER_PREFIX','')
    far=ce.get('CK_AR','').replace('${CK_ANDROID_COMPILER_PREFIX}',pr).replace('%CK_ANDROID_COMPILER_PREFIX%',pr)

    if far!='':
       par=os.path.join(pb,'bin',far)
       if not os.path.isfile(par) and ge.get('CK_ENV_COMPILER_GCC_BIN','')!='':
          par=os.path.join(ge['CK_ENV_COMPILER_GCC_BIN'],far)
       if os.path.isfile(par):
          ie['CK_AR_PATH_FOR_CMAKE']=par

    # Check Prefix
    pr=ce.get('CK_ANDROID_COMPILER_PREFIX','')
    if pr=='': pr=ge.get('CK_ANDROID_COMPILER_PREFIX','')

    # Set extra env for CMAKE based on ABI
    abi=tosd.get('abi','')
    cf=tosd.get('cpu_features',{})

    ie['CK_ARMEABI_V7A']='OFF'
    ie['CK_ARMEABI_V7A_HARD']='OFF'

    if abi=='armeabi-v7a':
       ie['CK_CMAKE_SYSTEM_PROCESSOR']='armv7-a'
       ck_cc2+=' -march=armv7-a '
       ck_cxx2+='  -march=armv7-a '

       if cf.get('arm_fp_hard','')=='yes':
          ie['CK_ARMEABI_V7A_HARD']='ON'
          ck_cc2+=' -mfloat-abi=hard -mhard-float '
          ck_cxx2+=' -mfloat-abi=hard -mhard-float '
       else:
          ie['CK_ARMEABI_V7A']='ON'
          ck_cc2+=' -mfloat-abi=softfp '
          ck_cxx2+=' -mfloat-abi=softfp '
    elif abi=='arm64-v8a':
       ie['CK_CMAKE_SYSTEM_PROCESSOR']='aarch64'

    # Extra CPU features
    # Current LLVM doesn't seem to support NEON
    if cf.get('arm_fp_neon','')=='yes' and 'clang' not in ck_cc:
       ie['CK_CPU_ARM_NEON']='ON'
    else:
       ie['CK_CPU_ARM_NEON']='OFF'

    if cf.get('arm_fp_vfpv3','')=='yes':
       ie['CK_CPU_ARM_VFPV3']='ON'
    else:
       ie['CK_CPU_ARM_VFPV3']='OFF'

    # Check LD
    fld=ce.get('CK_LD','')
    if fld=='': fld=ge.get('CK_LD','')

    if fld!='':
       fld=fld.replace('${CK_ANDROID_COMPILER_PREFIX}',pr).replace('%CK_ANDROID_COMPILER_PREFIX%',pr)
       pld=os.path.join(pb,'bin',fld)
       if not os.path.isfile(pld) and ge.get('CK_ENV_COMPILER_GCC_BIN','')!='':
          pld=os.path.join(ge['CK_ENV_COMPILER_GCC_BIN'],fld)
       if os.path.isfile(pld):
          ie['CK_LD_PATH_FOR_CMAKE']=pld

    # Add other obligatory flags
    ck_cc2+=' '+svarb+svarb1+'CK_COMPILER_FLAGS_OBLIGATORY'+svare1+svare
    ck_cxx2+=' '+svarb+svarb1+'CK_COMPILER_FLAGS_OBLIGATORY'+svare1+svare

    x=ce.get('CK_ENV_LIB_STDCPP_INCLUDE','')
    if x=='': x=ge.get('CK_ENV_LIB_STDCPP_INCLUDE','')
    if x!='': ck_cxx2+=' '+ce['CK_FLAG_PREFIX_INCLUDE']+x

    x=ce.get('CK_ENV_LIB_STDCPP_INCLUDE_EXTRA','')
    if x=='': x=ge.get('CK_ENV_LIB_STDCPP_INCLUDE_EXTRA','')
    if x!='': ck_cxx2+=' '+ce['CK_FLAG_PREFIX_INCLUDE']+x

    x=ce.get('CK_ENV_LIB_STDCPP','')
    if x=='': x=ge.get('CK_ENV_LIB_STDCPP','')
    if x!='': ck_cxx2+=' '+ce['CK_FLAG_PREFIX_LIB_DIR']+x

#    if ce.get('CK_ENV_LIB_STD','')!='':
#       ck_cc2+=' '+ce['CK_FLAG_PREFIX_LIB_DIR']+ce['CK_ENV_LIB_STD']
#       ck_cxx2+=' '+ce['CK_FLAG_PREFIX_LIB_DIR']+ce['CK_ENV_LIB_STD']

    # Cleaning flags
    ck_cc2=ck_cc2.strip()
    ck_cxx2=ck_cxx2.strip()

    if ck_cc2.find(' ')<0: ck_cc2='"'+ck_cc2+'"'
    if ck_cxx2.find(' ')<0: ck_cxx2='"'+ck_cxx2+'"'

    # New env variables (full path to compiler + extra flags)
    ie['CK_CC_PATH_FOR_CMAKE']=pb_cc
    ie['CK_CC_FLAGS_FOR_CMAKE']=ck_cc2

    ie['CK_CXX_PATH_FOR_CMAKE']=pb_cxx
    ie['CK_CXX_FLAGS_FOR_CMAKE']=ck_cxx2

    ie['CK_COMPILER_PATH_FOR_CMAKE']=os.path.join(pb,'bin')

    # I had problems with -frtti and -fexceptions in Caffe
    ie['CK_CC_FLAGS_ANDROID_TYPICAL']='-DANDROID'
    ie['CK_CXX_FLAGS_ANDROID_TYPICAL']='-DANDROID'

    y=''
    x=ce.get('CK_ENV_LIB_STDCPP_STATIC','')
    if x=='': x=ge.get('CK_ENV_LIB_STDCPP_STATIC','')
    y+=' '+x

    x=ce.get('CK_EXTRA_LIB_ATOMIC','')
    if x=='': x=ge.get('CK_EXTRA_LIB_ATOMIC','')
    y+=' '+x

    ie['CK_LINKER_LIBS_ANDROID_TYPICAL']=y.strip()

    return {'return':0, 'install_env':ie}
