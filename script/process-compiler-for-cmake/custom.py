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
    env=i.get('new_env',{})
    s=''

#    del(i['ck_kernel'])
#    r=ck.save_json_to_file({'json_file':'d:\\zzz1.json','dict':i})
#    exit(1)

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    hosn=hosd.get('ck_name2','')
    osn=tosd.get('ck_name2','')
    osn_mac=tosd.get('macos','')

    # Env vars on host
    svb=hosd.get('env_var_start','')+hosd.get('env_var_extra1','')
    sve=hosd.get('env_var_extra2','')+hosd.get('env_var_stop','')

    # Check platform
    hplat=hosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    phosd=hosd.get('ck_name','')

    ie={}

    iv=i.get('interactive','')
    cus=i.get('customize',{})
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})

    # Set default parameters from compiler deps
    cd=deps.get('compiler',{})
    if len(cd)==0 or 'dict' not in cd:
       cd=deps.get('host-compiler',{})
    if len(cd)==0 or 'dict' not in cd:
       return {'return':1, 'error':'"compiler" or "host-compiler" not found in deps'}

    cdd=cd['dict']
    ce=cdd['env']
    cep=cdd['customize']['env_prefix']

    ck_cc=ce.get('CK_CC','')
    ck_cxx=ce.get('CK_CXX','')

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
#    pb=ce.get(cep,'')
#    pb_cc=os.path.join(pb,'bin',ck_cc1)
#    pb_cxx=os.path.join(pb,'bin',ck_cxx1)

    pb=ce.get(cep,'')
    pb1=ce.get(cep+'_BIN','')

    if pb1=='' and phosd!='win':
       pb1='/usr/bin'

    pb_cc=os.path.join(pb1,ck_cc1)
    pb_cxx=os.path.join(pb1,ck_cxx1)

    if phosd=='win' and not pb_cc.endswith('.exe'):
       pb_cc+='.exe' # trying for windows

    if not os.path.isfile(pb_cc):
        return {'return':1, 'error':'can\'t find full path to compiler ('+pb_cc+') - can\'t be used with this CMake-based package'}

    if phosd=='win' and not pb_cxx.endswith('.exe'):
       pb_cxx+='.exe' # trying for windows

    if not os.path.isfile(pb_cxx):
        return {'return':1, 'error':'can\'t find full path to compiler ('+pb_cxx+') - can\'t be used with this CMake-based package'}

    # Check Prefix
    pr=ce.get('CK_ANDROID_COMPILER_PREFIX','')
    if pr=='': pr=ge.get('CK_ANDROID_COMPILER_PREFIX','')

    # Check AR
    far=ce.get('CK_AR','')

    if osn=='android':
       far=far.replace('${CK_ANDROID_COMPILER_PREFIX}',pr).replace('%CK_ANDROID_COMPILER_PREFIX%',pr)

    par=''
    if far!='':
       par=os.path.join(pb1,far)
       if not os.path.isfile(par) and ge.get('CK_ENV_COMPILER_GCC_BIN','')!='':
          par=os.path.join(ge['CK_ENV_COMPILER_GCC_BIN'],far)

    if phosd=='win' and not par.endswith('.exe'):
       par+='.exe' # trying for windows

    if (phosd!='win' or osn=='android') and os.path.isfile(par):
       ie['CK_AR_PATH_FOR_CMAKE']=par
       ie['CK_AR_PATH_FOR_CMAKE_MINGW']=par.replace('\\','/')
    else:
       par=''

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
          ck_cc2+=' -mfloat-abi=hard -mhard-float -Wl,--no-warn-mismatch'
          ck_cxx2+=' -mfloat-abi=hard -mhard-float -Wl,--no-warn-mismatch '
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

    pld=''

    if fld!='':
       fld=fld.replace('${CK_ANDROID_COMPILER_PREFIX}',pr).replace('%CK_ANDROID_COMPILER_PREFIX%',pr)
       pld=os.path.join(pb1,fld)
       if not os.path.isfile(pld) and ge.get('CK_ENV_COMPILER_GCC_BIN','')!='':
          pld=os.path.join(ge['CK_ENV_COMPILER_GCC_BIN'],fld)
       if phosd=='win' and not pld.endswith('.exe'):
          pld+='.exe' # trying for windows
       if (phosd!='win' and osn=='android') and os.path.isfile(pld):
          ie['CK_LD_PATH_FOR_CMAKE']=pld
          ie['CK_LD_PATH_FOR_CMAKE_MINGW']=pld.replace('\\','/')

    # Add other obligatory flags
    ck_cc2+=' '+svb+'CK_COMPILER_FLAGS_OBLIGATORY'+sve
    ck_cxx2+=' '+svb+'CK_COMPILER_FLAGS_OBLIGATORY'+sve

    # Check for MingW (mainly for boost on Windows)
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

#    if phosd!='win':
#       if ck_cc2.find(' ')>0: ck_cc2='"'+ck_cc2+'"'
#       if ck_cxx2.find(' ')>0: ck_cxx2='"'+ck_cxx2+'"'

    # New env variables (full path to compiler + extra flags)
    if hosn=='win' and osn=='android':
       pb_cc=pb_cc.replace('\\','/')
       pb_cxx=pb_cxx.replace('\\','/')

    ie['CK_CC_PATH_FOR_CMAKE']=pb_cc
    ie['CK_CC_PATH_FOR_CMAKE_MINGW']=pb_cc.replace('\\','/')
    ie['CK_CC_FLAGS_FOR_CMAKE']=ck_cc2
    ie['CK_CC_FLAGS_FOR_CMAKE_MINGW']=ck_cc2.replace('\\','/')

    ie['CK_CXX_PATH_FOR_CMAKE']=pb_cxx
    ie['CK_CXX_PATH_FOR_CMAKE_MINGW']=pb_cxx.replace('\\','/')

    ie['CK_CXX_FLAGS_FOR_CMAKE']=ck_cxx2
    ie['CK_CXX_FLAGS_FOR_CMAKE_MINGW']=ck_cxx2.replace('\\','/')

    ie['CK_COMPILER_PATH_FOR_CMAKE']=pb1
    ie['CK_COMPILER_PATH_FOR_CMAKE_MINGW']=pb1.replace('\\','/')



    # Typical Android flags
    # I had problems with -frtti and -fexceptions in Caffe
    ck_cc_andr='-DANDROID'
    ck_cxx_andr='-DANDROID'

    # Typical Android lib
    y=''
    x=ce.get('CK_ENV_LIB_STDCPP_STATIC','')
    if x=='': x=ge.get('CK_ENV_LIB_STDCPP_STATIC','')
    y+=' '+x

    x=ce.get('CK_EXTRA_LIB_ATOMIC','')
    if x=='': x=ge.get('CK_EXTRA_LIB_ATOMIC','')
    y+=' '+x

    y=y.strip()

    ck_libs_andr=y

#    if phosd!='win':
#       if ck_cc_andr.find(' ')>0: ck_cc_andr='"'+ck_cc_andr+'"'
#       if ck_cxx_andr.find(' ')>0: ck_cxx_andr='"'+ck_cxx_andr+'"'
#       if ck_libs_andr.find(' ')>0: ck_libs_andr='"'+ck_libs_andr+'"'

    if osn=='android':
       ie['CK_CC_FLAGS_ANDROID_TYPICAL']=ck_cc_andr
       ie['CK_CC_FLAGS_ANDROID_TYPICAL_MINGW']=ck_cc_andr.replace('\\','/')
       ie['CK_CXX_FLAGS_ANDROID_TYPICAL']=ck_cxx_andr
       ie['CK_CXX_FLAGS_ANDROID_TYPICAL_MINGW']=ck_cxx_andr.replace('\\','/')
       ie['CK_LINKER_LIBS_ANDROID_TYPICAL']=ck_libs_andr
       ie['CK_LINKER_LIBS_ANDROID_TYPICAL_MINGW']=ck_libs_andr.replace('\\','/')

    # Extra checks
    extra=''

    ienv=cfg.get('customize',{}).get('install_env',{})

    if hosn=='win':
       if osn=='android':
          extra+=' -G"MinGW Makefiles" -DCMAKE_MAKE_PROGRAM=make -DCMAKE_SYSTEM_NAME=Generic'
       else:
          par=''
          pld=''

          # Check generator by tags from Microsoft compiler
          cgen=env.get('CK_CMAKE_GENERATOR','')
          if cgen=='':
             cgen=ce.get('CK_CMAKE_GENERATOR','')
          if cgen=='':
             for k in cdd.get('deps',{}):
                 q=cdd['deps'][k]
                 tags=q.get('tags',[])
                 if 'compiler' in tags and 'microsoft' in tags:
                    cgen=q.get('dict',{}).get('env',{}).get('CK_CMAKE_GENERATOR','')

             if cgen=='':
                return {'return':1, 'error':'can\'t find CK_MAKE_GENERATOR in CK description of Microsoft compiler'}

          extra+='-G"'+cgen+'"'

          if 'clang' in ck_cc:
             # Check toolset
             ver=''
             vers={}
             for d in [os.environ.get('ProgramFiles',''), os.environ.get('ProgramFiles(x86)','')]:
                 if d!='':
                    d1=os.path.join(d, 'MSBuild\\Microsoft.Cpp\\v4.0')
                    if os.path.isdir(d1):
                       d2=os.listdir(d1)
                       for q in d2:
                           if q.startswith('V'):
                              vers[q[1:]]=os.path.join(d1,q)

             # Sort keys:
             if len(vers)>0:
                ver=sorted(list(vers.keys()), reverse=True)[0]

             if ver=='':
                return {'return':1, 'error':'can\'t find host MSBuild version'}

             xver=''
             if ver=='140':
                xver='vs2014'
             elif ver=='120':
                xver='vs2013'
             elif ver=='110':
                xver='vs2012'
             elif ver=='100':
                xver='vs2010'
             else:
                return {'return':1, 'error':'unknown MSBuild version ('+ver+')'}

             # Hack -  and add correct names (in ck detect soft:compiler.microsoft)
             extra+=' -T"LLVM-'+xver+'"'

          elif 'icl' in ck_cc:
             # Hack - should detect intel version correctly and add correct names (in ck detect soft:compiler.icc)
             extra+=' -T"Intel C++ Compiler XE 15.0"'

          extra+=' '+ienv.get('PACKAGE_CONFIGURE_FLAGS_WINDOWS','')

    elif osn=='linux':
       extra+=' '+ienv.get('PACKAGE_CONFIGURE_FLAGS_LINUX','')

    if osn=='android':
       extra+=' '+ienv.get('PACKAGE_CONFIGURE_FLAGS_ANDROID','')

    ie['CK_CMAKE_EXTRA']=extra.strip()

    # Update PACKAGE URL and checkout if needed
    x1=''
    x2=''
    if osn=='android':
       x1='PACKAGE_URL_ANDROID'
       x2='PACKAGE_GIT_CHECKOUT_ANDROID'
    elif osn=='win':
       x1='PACKAGE_URL_WINDOWS'
       x2='PACKAGE_GIT_CHECKOUT_WINDOWS'
    elif osn=='linux':
       x1='PACKAGE_URL_LINUX'
       x2='PACKAGE_GIT_CHECKOUT_LINUX'
       if osn_mac=='yes':
          if ienv.get('PACKAGE_URL_MACOS','')!='':
             x1='PACKAGE_URL_MACOS'
          if ienv.get('PACKAGE_GIT_CHECKOUT_MACOS','')!='':
             x2='PACKAGE_GIT_CHECKOUT_MACOS'

    if x1!='' and ienv.get(x1,'')!='':
       ie['PACKAGE_URL']=ienv[x1]
    if x2!='' and ienv.get(x2,'')!='':
       ie['PACKAGE_GIT_CHECKOUT']=ienv[x2]

    return {'return':0, 'install_env':ie}
