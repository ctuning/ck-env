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

    svarb=hosd.get('env_var_start','')
    svarb1=hosd.get('env_var_extra1','')
    svare=hosd.get('env_var_stop','')
    svare1=hosd.get('env_var_extra2','')

    iv=i.get('interactive','')
    cus=i.get('customize',{})
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})

    # Set default parameters
    cd=deps['compiler']

    cdd=cd['dict']
    ce=cdd['env']
    cep=cdd['customize']['env_prefix']

    ck_cc=ce['CK_CC']
    ck_cxx=ce['CK_CXX']

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

    # Add other obligatory flags
    ck_cc2+=' '+svarb+svarb1+'CK_COMPILER_FLAGS_OBLIGATORY'+svare1+svare
    ck_cxx2+=' '+svarb+svarb1+'CK_COMPILER_FLAGS_OBLIGATORY'+svare1+svare

    if ce.get('CK_ENV_LIB_STDCPP_INCLUDE','')!='':
       ck_cxx2+=' '+ce['CK_FLAG_PREFIX_INCLUDE']+svarb+svarb1+'CK_ENV_LIB_STDCPP_INCLUDE'+svare1+svare
    if ce.get('CK_ENV_LIB_STDCPP_INCLUDE_EXTRA','')!='':
       ck_cxx2+=' '+ce['CK_FLAG_PREFIX_INCLUDE']+svarb+svarb1+'CK_ENV_LIB_STDCPP_INCLUDE_EXTRA'+svare1+svare
    if ce.get('CK_ENV_LIB_STDCPP','')!='':
       ck_cxx2+=' '+ce['CK_FLAG_PREFIX_LIB_DIR']+ce['CK_ENV_LIB_STDCPP']

#    if ce.get('CK_ENV_LIB_STD','')!='':
#       ck_cc2+=' '+ce['CK_FLAG_PREFIX_LIB_DIR']+ce['CK_ENV_LIB_STD']
#       ck_cxx2+=' '+ce['CK_FLAG_PREFIX_LIB_DIR']+ce['CK_ENV_LIB_STD']

    # Cleaning flags
    ck_cc2=ck_cc2.strip()
    ck_cxx2=ck_cxx2.strip()

    if ck_cc2.find(' ')<0: ck_cc2='"'+ck_cc2+'"'
    if ck_cxx2.find(' ')<0: ck_cxx2='"'+ck_cxx2+'"'

    # New env variables (full path to compiler + extra flags)
    ie={}

    ie['CK_CC_PATH_FOR_CMAKE']=pb_cc
    ie['CK_CC_FLAGS_FOR_CMAKE']=ck_cc2

    ie['CK_CXX_PATH_FOR_CMAKE']=pb_cxx
    ie['CK_CXX_FLAGS_FOR_CMAKE']=ck_cxx2

    ie['CK_COMPILER_PATH_FOR_CMAKE']=os.path.join(pb,'bin')

    return {'return':0, 'install_env':ie}
