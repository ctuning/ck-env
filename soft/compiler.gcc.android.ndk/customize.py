#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

##############################################################################
# customize directories to automatically find and register software

import os

def dirs(i):
    return {'return':0}

##############################################################################
# prepare env

def version_cmd(i):

    fp=i['full_path']
    cmdx=i['cmd']

    cmd=fp+' '+cmdx

    return {'return':0, 'cmd':cmd}

##############################################################################
# limit directories 

def limit(i):

    hosd=i.get('host_os_dict',{})
    tosd=i.get('target_os_dict',{})

    phosd=hosd.get('ck_name','')
    hbits=hosd.get('bits','')
    tbits=tosd.get('bits','')

    prebuilt=''
    if phosd=='win':
       if hbits=='64':
          prebuilt='windows-x86_64'
       else:
          prebuilt='windows-x86'
    else:
       if hbits=='64':
          prebuilt='linux-x86_64'
       else:
          prebuilt='linux-x86'

    acp=tosd.get('android_compiler_prefix','')
    if acp=='':
       return {'return':1, 'error':'android_compiler_prefix is not specified in target OS meta'}

    fn=acp+'-gcc'
    if phosd=='win':
       fn+='.exe'

    atc=tosd.get('android_toolchain','')
    if atc=='':
       return {'return':1, 'error':'android_toolchain is not specified in target OS meta'}

    dr=i.get('list',[])
    drx=[]

    for q in dr:
        p0=os.path.dirname(q)
        p1=os.path.join(p0,'toolchains')
        if os.path.isdir(p1):
           x=[]
           try:
              x=os.listdir(p1)
           except:
              pass

           for f in x:
               if f.startswith(atc+'-') and f.find('clang')<0:
                  p2=os.path.join(p1,f,'prebuilt',prebuilt,'bin',fn)
                  if os.path.isfile(p2):
                     drx.append(p2)

    return {'return':0, 'list':drx}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip()
        if q!='':
           j=q.lower().find(') ')
           if j>0:
              q=q[j+2:]
              j=q.find(' ')
              if j>0:
                 q=q[:j]
              ver=q
              break

    return {'return':0, 'version':ver}

##############################################################################
# setup environment setup

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
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    import os

    # Get variables
    ck=i['ck_kernel']
    s=''

    iv=i.get('interactive','')

    env=i.get('env',{})
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})
    tags=i.get('tags',[])
    cus=i.get('customize',{})

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    hplat=hosd.get('ck_name','')
    hbits=hosd.get('bits','')
    tbits=tosd.get('bits','')

    target_d=i.get('target_os_dict',{})
    winh=hosd.get('windows_base','')
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    eqis=hosd.get('env_quotes_if_space','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    fp=cus.get('full_path','')

    ############################################################
    platform=target_d.get('android_ndk_platform','')
    if platform=='':
       return {'return':1, 'error':'platform is not defined in target OS'}

    api_level=''
    j=platform.rfind('-')
    if j>0:
        api_level=platform[j+1:].strip()

    ############################################################
    arch=target_d.get('android_ndk_arch','')
    if arch=='':
       return {'return':1, 'error':'platform architecture is not defined in target OS'}

    ############################################################
    abi=target_d.get('abi','')
    if arch=='':
       return {'return':1, 'error':'abi is not defined in target OS'}

    ############################################################
    atc=tosd.get('android_toolchain','')
    if atc=='':
       return {'return':1, 'error':'android_toolchain is not specified in target OS meta'}

    acp=tosd.get('android_compiler_prefix','')
    if acp=='':
       return {'return':1, 'error':'android_compiler_prefix is not specified in target OS meta'}

    env['CK_ANDROID_COMPILER_PREFIX']=acp
    env['CK_ANDROID_TOOLCHAIN']=atc
    env['CK_ANDROID_ABI']=abi
    env['CK_CPU_BITS']=tbits
    env['CK_ANDROID_API_LEVEL']=api_level
    env['CK_ANDROID_NDK_ARCH']=arch
    env['CK_ANDROID_NDK_PLATFORM']=platform

    # Check path
    ep=cus.get('env_prefix','')
    if fp!='':
       p1=os.path.dirname(fp)
       p2=os.path.dirname(p1)
       p3=os.path.dirname(p2)
       p4=os.path.dirname(p3)
       p5=os.path.dirname(p4)
       pi=os.path.dirname(p5)

       if winh=='yes':
          s+='\nset PATH='+pi+';%PATH%\n\n'
       else:
          s+='\nexport PATH='+pi+':$PATH\n\n'

       if ep!='':
          env[ep]=p2
          env[ep+'_BIN']=p1

       prebuilt=''
       if hplat=='win':
          if hbits=='64':
             prebuilt='windows-x86_64'
          else:
             prebuilt='windows-x86'
       else:
          if hbits=='64':
             prebuilt='linux-x86_64'
          else:
             prebuilt='linux-x86'

       cus['tool_prefix_configured']='yes'
       cus['tool_prefix']=acp+'-'
       cus['platform_path_configured']='yes'
       cus['platform_path']=os.path.join(pi,'platforms')
       cus['add_extra_path_configured']='yes'
       cus['add_extra_path']=os.path.join(pi,'prebuilt',prebuilt,'bin')

       cus['ef_configured']='yes'
       x=''
#       if arch=='arm64': 
       x='-fPIE -pie'
       cus['ef']=x

       j=p4.find(atc)
       if j>0:
          ver=p4[j+len(atc)+1:]

          cus['libstdcpppath_include_configured']='yes'
          cus['libstdcpppath_include']=os.path.join(pi,'sources','cxx-stl','gnu-libstdc++',ver,'include')

          cus['libstdcpppath_configured']='yes'
          cus['libstdcpppath']=os.path.join(pi,'sources','cxx-stl','gnu-libstdc++',ver,'libs',abi)

    env.update({
      "CK_AR": "$#tool_prefix#$ar", 
      "CK_ASM_EXT": ".s", 
      "CK_CC": "$#tool_prefix#$gcc", 
      "CK_COMPILER_FLAGS_OBLIGATORY": "", 
      "CK_COMPILER_FLAG_CPP11": "-std=c++11", 
      "CK_COMPILER_FLAG_CPP0X": "-std=c++0x", 
      "CK_COMPILER_FLAG_GPROF": "-pg", 
      "CK_COMPILER_FLAG_OPENMP": "-fopenmp", 
      "CK_COMPILER_FLAG_PLUGIN": "-fplugin=", 
      "CK_COMPILER_FLAG_PTHREAD_LIB": "-lpthread", 
      "CK_CXX": "$#tool_prefix#$g++", 
      "CK_OPT_ALL_WARNINGS": "-Wall", 
      "CK_DLL_EXT": ".so", 
      "CK_EXE_EXT": ".out", 
      "CK_EXTRA_LIB_Z": "-lz", 
      "CK_EXTRA_LIB_LOG": "-llog", 
      "CK_EXTRA_LIB_DL": "-ldl", 
      "CK_EXTRA_LIB_M": "-lm", 
      "CK_FLAGS_CREATE_ASM": "-S", 
      "CK_FLAGS_CREATE_OBJ": "-c", 
      "CK_FLAGS_DLL": "-shared -fPIC", 
      "CK_FLAGS_DLL_EXTRA": "", 
      "CK_FLAGS_OUTPUT": "-o ", 
      "CK_FLAGS_STATIC_BIN": "-static -fPIC", 
      "CK_FLAGS_STATIC_LIB": "-fPIC", 
      "CK_FLAG_PREFIX_INCLUDE": "-I", 
      "CK_FLAG_PREFIX_LIB_DIR": "-L", 
      "CK_FLAG_PREFIX_VAR": "-D", 
      "CK_GPROF_OUT_FILE": "gmon.out", 
      "CK_LB": "$#tool_prefix#$ar rcs", 
      "CK_LB_OUTPUT": "", 
      "CK_LD": "$#tool_prefix#$ld", 
      "CK_LD_FLAGS_EXTRA": "", 
      "CK_LIB_EXT": ".a", 
      "CK_LINKER_FLAG_OPENMP": "-lgomp", 
      "CK_MAKE": "make", 
      "CK_OBJDUMP": "$#tool_prefix#$objdump -d", 
      "CK_OBJ_EXT": ".o", 
      "CK_OPT_SIZE": "-Os", 
      "CK_OPT_SPEED": "-O3", 
      "CK_OPT_SPEED_SAFE": "-O2", 
      "CK_PLUGIN_FLAG": "-fplugin=", 
      "CK_PROFILER": "gprof"
    })

    ############################################################
    # Ask a few more questions

    ############################################################
    prefix_configured=cus.get('tool_prefix_configured','')
    prefix=cus.get('tool_prefix','')
    if prefix_configured!='yes' and iv=='yes':
       if prefix!='':
          ck.out('Current compiler name prefix: '+prefix)
       else:
          ra=ck.inp({'text':'Enter compiler name prefix, if needed (such as aarch64-linux-android-): '})
          prefix=ra['string'].strip()
          cus['tool_prefix_configured']='yes'

    if prefix!='':
       env['CK_COMPILER_PREFIX']=prefix
       cus['tool_prefix']=prefix
       cus['tool_prefix_configured']='yes'

    for k in env:
        v=env[k]
        v=v.replace('$#tool_prefix#$',prefix)
        env[k]=v

    ############################################################
    extra_path_configured=cus.get('add_extra_path_configured','')
    extra_path=cus.get('add_extra_path','')
    if extra_path_configured!='yes' and iv=='yes':
       if extra_path!='':
          ck.out('Full path to pre-built Android tools: '+extra_path)
       else:
          ra=ck.inp({'text':'Enter full path to pre-built Android tools (such as ...prebuilt/linux-x86_64/bin) : '})
          extra_path=ra['string']
          cus['extra_path_configured']='yes'

    if extra_path!='':
       cus['add_extra_path']=extra_path
       cus['add_extra_path_configured']='yes'

    if extra_path!='':
       if winh=='yes':
          s+='\nset PATH='+extra_path+';%PATH%\n\n'
       else:
          s+='\nexport PATH='+extra_path+':$PATH\n\n'

    ############################################################
    platform_path_configured=cus.get('platform_path_configured','')
    platform_path=cus.get('platform_path','')
    if platform_path_configured!='yes' and iv=='yes':
       if platform_path!='':
          ck.out('Full path to directory with Android NDK platforms: '+platform_path)
       else:
          ra=ck.inp({'text':'Enter full path to directory with Android NDK platforms : '})
          platform_path=ra['string']
          cus['platform_path_configured']='yes'

    if platform_path=='':
       return {'return':1, 'error':'path to Android platforms is not defined'}

    cus['platform_path']=platform_path
    cus['platform_path_configured']='yes'

    ############################################################
    libstdcpppathi_configured=cus.get('libstdcpppath_include_configured','')
    libstdcpppathi=cus.get('libstdcpppath_include','')
    if libstdcpppathi_configured!='yes' and iv=='yes':
       if libstdcpppathi!='':
          ck.out('Full path to include directory with libstdc++: '+libstdcpppathi)
       else:
          ra=ck.inp({'text':'* If needed, enter full path to include directory with libstdc++ (such as ...sources/cxx-stl/gnu-libstdc++/4.9/include: '})
          libstdcpppathi=ra['string']
          cus['libstdcpppath_include_configured']='yes'

    cus['libstdcpppath_include']=libstdcpppathi
    env['CK_ENV_LIB_STDCPP_INCLUDE']=libstdcpppathi
    cus['libstdcpppath_include_configured']='yes'

    libstdcpppath_configured=cus.get('libstdcpppath_configured','')
    libstdcpppath=cus.get('libstdcpppath','')
    if libstdcpppath_configured!='yes' and iv=='yes':
       if libstdcpppath!='':
          ck.out('Full path to include directory with libstdc++: '+libstdcpppath)
       else:
          ra=ck.inp({'text':'* If needed, enter full path to lib directory with libstdc++ (such as ...sources/cxx-stl/gnu-libstdc++/4.9/libs/armeabi-v7a: '})
          libstdcpppath=ra['string']
          cus['libstdcpppath_configured']='yes'

    if winh=='yes':
       sep='\\'
    else:
       sep='/'

    cus['libstdcpppath']=libstdcpppath
    if libstdcpppath!='':
       env['CK_ENV_LIB_STDCPP_STATIC']=libstdcpppath+sep+'libgnustl_static.a'
       env['CK_ENV_LIB_STDCPP_DYNAMIC']=libstdcpppath+sep+'libgnustl_shared.so'
       env['CK_ENV_LIB_STDCPP_INCLUDE_EXTRA']=libstdcpppath+sep+'include'
    else:
       env['CK_ENV_LIB_STDCPP_STATIC']=''
       env['CK_ENV_LIB_STDCPP_DYNAMIC']=''
       env['CK_ENV_LIB_STDCPP_INCLUDE_EXTRA']=''
    cus['libstdcpppath_configured']='yes'

    ############################################################
    ef_configured=cus.get('ef_configured','')
    ef=cus.get('ef','')
    if ef_configured!='yes' and iv=='yes':
       ra=ck.inp({'text':'Force extra flags, if needed (such as -fPIE -pie for aarch64): '})
       ef=ra['string']
       cus['ef']=ef
       cus['ef_configured']='yes'

    ##############
    if winh=='yes':
       psysroot=platform_path+'\\'+platform+'\\arch-'+arch
    else:
       psysroot=platform_path+'/'+platform+'/arch-'+arch
    sysroot='--sysroot "'+psysroot+'"'

    env['CK_SYS_ROOT']=psysroot

    x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
    if sysroot not in x:
       x=sysroot+' '+x
    env['CK_COMPILER_FLAGS_OBLIGATORY']=x

    if ef!='':
       x=env['CK_CC']
       if x.find(ef)<0:
          x=eqis+x+' '+ef+eqis
       env['CK_CC']=x

       x=env['CK_CXX']
       if x.find(ef)<0:
          x=eqis+x+' '+ef+eqis
       env['CK_CXX']=x

    if pi!='':
       env['CK_ANDROID_NDK_ROOT_DIR']=pi

#    x=env.get('CK_LD_FLAGS_EXTRA','')
#    if sysroot not in x:
#       x=sysroot+' '+x
#    env['CK_LD_FLAGS_EXTRA']=x

    return {'return':0, 'bat':s, 'env':env, 'tags':tags, 'cus':cus}
