#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os

##############################################################################
# customize directories to automatically find and register software

def dirs(i):
    hosd=i['host_os_dict']
    phosd=hosd.get('ck_name','')
    dirs=i.get('dirs', [])
    if phosd=='win':
        win_dir = 'C:\\Users\\All Users\\Microsoft'
        if os.path.isdir(win_dir):
            dirs.append(win_dir)
    return {'return':0, 'dirs':dirs}

##############################################################################
# prepare env

def version_cmd(i):

    fp=i['full_path']
    cmdx=i['cmd']

    if ' ' in fp:
       fp='"'+fp+'"'

    cmd=fp+' '+cmdx

    return {'return':0, 'cmd':cmd}

##############################################################################
# limit directories 

def limit(i):

    hosd=i.get('host_os_dict',{})
    tosd=i.get('target_os_dict',{})

    phosd=hosd.get('ck_name','')
    macos=hosd.get('macos', '')
    hbits=hosd.get('bits','')
    tbits=tosd.get('bits','')

    long_os_name = 'windows' if phosd=='win' else ('darwin' if macos else 'linux')
    prebuilt     = long_os_name + '-x86' + ('_64' if hbits=='64' else '')

    acp=tosd.get('android_compiler_prefix','')
    if acp=='':
       return {'return':1, 'error':'android_compiler_prefix is not specified in target OS meta'}

    atc=tosd.get('android_toolchain','')
    if atc=='':
       return {'return':1, 'error':'android_toolchain is not specified in target OS meta'}

    fn='clang'
    if phosd=='win':
       fn+='.exe'

    dr=i.get('list',[])
    drx=[]

    for q in dr:
        p0=os.path.dirname(q)
        p1=os.path.join(p0,'toolchains','llvm','prebuilt',prebuilt,'bin',fn)
        if os.path.isfile(p1):
           if p1 not in drx:
              drx.append(p1)

    return {'return':0, 'list':drx}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip().lower()
        if q!='':
           j=q.find(' version ')
           if j>0 and (q.startswith('clang') or q.startswith('android clang')):
              q=q[j+9:]
              j=q.find(' ')
              if j>0:
                 q=q[:j]
              ver=q
              break

           j=q.find('clang version ')
           if j>0:
              j1=q.find(' ', j+14)
              if j1>0:
                 ver=q[j+14:j1].strip()
                 break

    if ver=='':
        ck.out('')
        ck.out('  WARNING: can\'t detect clang version from the following output:')
        for q in lst:
            ck.out('    '+q)
        ck.out('')

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

    fos=i.get('features',{}).get('os',{})
    os_name_long=fos.get('name_long','')

    iv=i.get('interactive','')

    env=i['env']
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})
    tags=i['tags']
    cus=i['customize']

    hos=i['host_os_uid']
    tos=i['host_os_uid']
    tdid=i['target_device_id']

    hosd=i.get('host_os_dict',{})
    target_d=i.get('target_os_dict',{})
    winh=hosd.get('windows_base','')
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    sdirs=hosd.get('dir_sep','')

    hplat=hosd.get('ck_name','')
    macos=hosd.get('macos','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    fp=cus.get('full_path','')

    tp=''

    arch=target_d.get('android_ndk_arch','')

    # Check NDK
    ndk_gcc=deps.get('ndk-gcc', {})
    ndk_gcc_env=ndk_gcc.get('dict',{}).get('env',{})

    ndk=ndk_gcc_env.get('CK_SYS_ROOT','')
    ndk_ver=''
    ndk_iver=0

    j=ndk.find('android-ndk-r')
    if j>=0:
       j1=ndk.find('/', j+1)
       j2=ndk.find('\\', j+1)
       if j2>=0 and j1>j2:
          j1=j2
       ndk_ver=ndk[j+13:j1]

       if len(ndk_ver)==3:
          ndk_iver=ck.safe_int(ndk_ver[:2],0)

    # Need to check that if path has spaces on Windows, then convert to non-space format, 
    # otherwise many issues with CMAKE ...
    if winh=='yes' and ' ' in fp:
       cmd='@for %%A in ("'+fp+'") do echo %%~sA'

       r=ck.access({'action':'shell',
                    'module_uoa':'os',
                    'host_os':hos,
                    'target_os':tos,
                    'device_id':tdid,
                    'cmd':cmd,
                    'split_to_list':'yes'})
       if r['return']>0: return r
       x=r['stdout_lst']

       if len(x)>2 and x[0]=='':
          y=x[2]
       if len(y)>0:
          pp1=os.path.dirname(fp)
          pp2=os.path.dirname(pp1)
          pp3=os.path.dirname(pp2)
          pp4=os.path.dirname(pp3) # since later will need real long name (to detect arch)

          fp=y

          ck.out('')
          ck.out('  Removed spaces from Windows path: '+fp)
          ck.out('')

    # Check path
    ep=cus.get('env_prefix','')
    if ep!='' and fp!='':
       p1=os.path.dirname(fp)
       pi=os.path.dirname(p1)
       p2=os.path.dirname(pi)
       p3=os.path.dirname(p2)
       p4=os.path.dirname(p3)
       p5=os.path.dirname(p4)

       ndk_path=p5
       ver=ndk_gcc.get('ver', '')[:-2]
       abi=target_d.get('abi','')

       env[ep]=pi
       env[ep+'_BIN']=p1

       pxl_gnustl_static = os.path.join(ndk_path, 'sources', 'cxx-stl', 'gnu-libstdc++', ver, 'libs', abi, 'libgnustl_static.a')
       pxl_gnustl_shared = os.path.join(ndk_path, 'sources', 'cxx-stl', 'gnu-libstdc++', ver, 'libs', abi, 'libgnustl_shared.so')

       if ndk_iver>=17:
          ck.out('')
          ck.out('NDK version '+str(ndk_iver)+' >= 17 - using LLVM C++ library ...')

          pxi=os.path.join(ndk_path, 'sources', 'cxx-stl', 'llvm-libc++', 'include')
          if not os.path.isdir(pxi):
             return {'return':1, 'error':'LLVM C++ include path not found: '+pxi}

          env['CK_ENV_LIB_STDCPP_INCLUDE']=pxi
          pxai=os.path.join(ndk_path, 'sources', 'cxx-stl', 'llvm-libc++abi', 'include')
          if not os.path.isdir(pxai):
             return {'return':1, 'error':'LLVM C++ include path not found: '+pxai}

          env['CK_ENV_LIB_STDCPP_INCLUDE_EXTRA']=pxai

          pxl_static=os.path.join(ndk_path, 'sources', 'cxx-stl', 'llvm-libc++', 'libs', abi, 'libc++_static.a')
          if not os.path.isfile(pxl_static):
             return {'return':1, 'error':'LLVM C++ lib not found: '+pxl_static}

          pxla_static=os.path.join(ndk_path, 'sources', 'cxx-stl', 'llvm-libc++', 'libs', abi, 'libc++abi.a')
          if not os.path.isfile(pxla_static):
             return {'return':1, 'error':'LLVM C++ lib not found: '+pxla_static}

          env['CK_ENV_LIB_STDCPP_STATIC']   = pxl_static+' '+pxla_static

          pxl_shared=os.path.join(ndk_path, 'sources', 'cxx-stl', 'llvm-libc++', 'libs', abi, 'libc++_shared.so')
          if not os.path.isfile(pxl_shared):
             return {'return':1, 'error':'LLVM C++ lib not found: '+pxl_shared}

          env['CK_ENV_LIB_STDCPP_DYNAMIC']  = pxl_shared

          env['CK_ENV_LIB_GNUSTL_STATIC']   = pxl_gnustl_static
          env['CK_ENV_LIB_GNUSTL_DYNAMIC']  = pxl_gnustl_shared

       else:
          env['CK_ENV_LIB_STDCPP_INCLUDE']=os.path.join(ndk_path, 'sources', 'cxx-stl', 'gnu-libstdc++', ver, 'include')
          env['CK_ENV_LIB_STDCPP_INCLUDE_EXTRA']=os.path.join(ndk_path, 'sources', 'cxx-stl', 'gnu-libstdc++', ver, 'libs', abi, 'include')
          env['CK_ENV_LIB_STDCPP_STATIC']   = pxl_gnustl_static
          env['CK_ENV_LIB_STDCPP_DYNAMIC']  = pxl_gnustl_shared
       cus['path_lib']=pi+sdirs+'lib'
       cus['path_include']=pi+sdirs+'include'

#       if ndk_gcc_env.get('CK_ENV_LIB_STDCPP_STATIC','')!='':
#          env['CK_ENV_LIB_STDCPP_STATIC']=ndk_gcc_env['CK_ENV_LIB_STDCPP_STATIC']
#       if ndk_gcc_env.get('CK_ENV_LIB_STDCPP_DYNAMIC','')!='':
#          env['CK_ENV_LIB_STDCPP_DYNAMIC']=ndk_gcc_env['CK_ENV_LIB_STDCPP_DYNAMIC']
#       if ndk_gcc_env.get('CK_ENV_LIB_STDCPP_INCLUDE_EXTRA','')!='':
#          env['CK_ENV_LIB_STDCPP_INCLUDE_EXTRA']=ndk_gcc_env['CK_ENV_LIB_STDCPP_INCLUDE_EXTRA']

       if hplat=='linux':
          sname=cus.get('soft_file',{}).get(hplat,'')
          pname=os.path.basename(fp)
          if pname.startswith(sname+'-'):
             tp=pname[len(sname):]

       if cus.get('tool_prefix','')=='':
          cus['tool_prefix_configured']='yes'
          cus['tool_prefix']=''
       if cus.get('tool_postfix','')=='':
          cus['tool_postfix_configured']='yes'
          cus['tool_postfix']=tp
       if cus.get('retarget','')=='':
          cus['retarget']='no'


    ############################################################
    if winh=='yes':

       env.update({
             "CK_AFTER_COMPILE_TO_BC": "ren *.o *", 
             "CK_ASM_EXT": ".s", 
             "CK_BC_EXT": ".bc", 
             "CK_COMPILER_ENABLE_EXCEPTIONS": "-fcxx-exceptions",
             "CK_CC": "$#tool_prefix#$clang", 
             "CK_COMPILER_FLAG_CPP17": "-std=c++17",
             "CK_COMPILER_FLAG_CPP14": "-std=c++14",
             "CK_COMPILER_FLAG_CPP11": "-std=c++11", 
             "CK_COMPILER_FLAG_CPP0X": "-std=c++0x", 
             "CK_COMPILER_FLAG_OPENMP": "-fopenmp", 
             "CK_COMPILER_FLAG_PTHREAD_LIB": "-lpthread", 
             "CK_COMPILER_FLAG_STD90": "-std=c90", 
             "CK_COMPILER_FLAG_STD99": "-std=c99", 
             "CK_CXX": "$#tool_prefix#$clang++", 
             "CK_F90": "", 
             "CK_F95": "", 
             "CK_FC": "", 
             "CK_FLAGS_CREATE_ASM": "-S", 
             "CK_FLAGS_CREATE_BC": "-c -emit-llvm", 
             "CK_FLAGS_CREATE_OBJ": "-c", 
             "CK_FLAGS_DYNAMIC_BIN": "", 
             "CK_FLAGS_OUTPUT": "-o", 
             "CK_FLAG_PREFIX_INCLUDE": "-I", 
             "CK_FLAG_PREFIX_LIB_DIR": "-L", 
             "CK_FLAG_PREFIX_VAR": "-D", 
             "CK_LINKER_FLAG_OPENMP": "-fopenmp", 
             "CK_MAKE": "nmake", 
             "CK_OBJ_EXT": ".o", 
             "CK_OPT_SIZE": "-Os", 
             "CK_OPT_SPEED": "-O3", 
             "CK_OPT_SPEED_SAFE": "-O2", 
             "CK_PLUGIN_FLAG": "-fplugin=", 
             "CM_INTERMEDIATE_OPT_TOOL": "opt", 
             "CM_INTERMEDIATE_OPT_TOOL_OUT": "-o",
             "CK_FLAGS_DLL_NO_LIBCMT": " ", 
           }) 

       # Modify if Android
       if remote=='yes':
          env.update({
             "CK_AR": "%CK_ANDROID_COMPILER_PREFIX%-ar", 
             "CK_COMPILER_FLAG_GPROF": "-pg", 
             "CK_DLL_EXT": ".so", 
             "CK_EXE_EXT": ".out", 
             "CK_EXTRA_LIB_DL": "-ldl", 
             "CK_EXTRA_LIB_M": "-lm", 
             "CK_FLAGS_DLL": "-shared -fPIC", 
             "CK_FLAGS_DLL_EXTRA": "", 
             "CK_FLAGS_STATIC_BIN": "-static -fPIC", 
             "CK_FLAGS_STATIC_LIB": "-fPIC", 
             "CK_LB": "%CK_ANDROID_COMPILER_PREFIX%-ar rcs", 
             "CK_LB_OUTPUT": "-o ", 
             "CK_LD_FLAGS_EXTRA": "", 
             "CK_LIB_EXT": ".a", 
             "CK_LD_DYNAMIC_FLAGS": "", 
             "CK_LD_FLAGS_EXTRA": "", 
             "CK_OBJDUMP": "%CK_ANDROID_COMPILER_PREFIX%-objdump -d",
             "CK_PROFILER": "gprof"})
       else:
          env.update({
             "CK_AR": "lib", 
             "CK_DLL_EXT": ".dll", 
             "CK_EXE_EXT": ".exe", 
             "CK_EXTRA_LIB_DL": "", 
             "CK_EXTRA_LIB_M": "", 
             "CK_FLAGS_DLL": "", 
             "CK_FLAGS_DLL_EXTRA": "-Xlinker /dll", 
             "CK_FLAGS_STATIC_BIN": "-static -Wl,/LARGEADDRESSAWARE:NO", 
             "CK_FLAGS_STATIC_LIB": "-fPIC", 
             "CK_LB": "lib", 
             "CK_LB_OUTPUT": "/OUT:", 
             "CK_LD_DYNAMIC_FLAGS": "", 
             "CK_LD_FLAGS_EXTRA": "", 
             "CK_LIB_EXT": ".lib", 
             "CK_OBJDUMP": "llvm-objdump -d"})

       prefix_configured=cus.get('tool_prefix_configured','')
       prefix=cus.get('tool_prefix','')

       if prefix!='':
          env['CK_COMPILER_PREFIX']=prefix
          cus['tool_prefix']=prefix
          cus['tool_prefix_configured']='yes'

       for k in env:
           v=env[k]
           v=v.replace('$#tool_prefix#$',prefix)
           env[k]=v

       retarget=cus.get('retarget','')
       lfr=cus.get('linking_for_retargeting','')

       if remote=='yes':
          ### Android target #########################################################

#          x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
          y='-target %CK_ANDROID_TOOLCHAIN% -gcc-toolchain %CK_ENV_COMPILER_GCC% --sysroot=%CK_SYS_ROOT%'

          x=''
#          if arch=='arm64': 
#             x='-fPIE -pie '
          x='-fPIE -pie '

          env["CK_COMPILER_FLAGS_OBLIGATORY"]=x+y
       else:
          env["CK_COMPILER_FLAGS_OBLIGATORY"]="-DWINDOWS"

          if retarget=='yes' and lfr!='':
             cus['linking_for_retargeting']=lfr
             env['CK_LD_FLAGS_EXTRA']=lfr

             add_m32=cus.get('add_m32','')
             if env.get('CK_COMPILER_ADD_M32','').lower()=='yes' or os.environ.get('CK_COMPILER_ADD_M32','').lower()=='yes':
                add_m32='yes'
                cus['add_m32']='yes'

#             if add_m32=='' and iv=='yes' and tbits=='32':
#                ra=ck.inp({'text':'Target OS is 32 bit. Add -m32 to compilation flags (y/N)? '})
#                x=ra['string'].strip().lower()
#                if x=='y' or x=='yes': 
#                   add_m32='yes'
#                   cus['add_m32']='yes'

             x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
             if remote!='yes':
                if x.find('-DWINDOWS')<0: 
                   x+=' -DWINDOWS' 
             if tbits=='32' and add_m32=='yes' and x.find('-m32')<0: 
                x+=' -m32' 

             y=cus.get('add_to_ck_compiler_flags_obligatory','')
             if y!='' and x.find(y)<0:
                x+=' '+y

             y='-target i686-pc-windows-msvc'
             if tbits=='64': y='-target x86_64-pc-windows-msvc'
             if x.find(y)<0:
                x+=' '+y

             if mingw=='yes': env['CK_MAKE']='mingw32-make'

             env['CK_COMPILER_FLAGS_OBLIGATORY']=x

       x=env.get('CK_CXX','')
       if x!='' and x.find('-fpermissive')<0:
          x+=' -fpermissive'
       env['CK_CXX']=x

       x=cus.get('add_extra_path','')
       if x!='':
          s+='\nset PATH='+pi+x+';%PATH%\n\n'

    else:
       ### Linux Host  #########################################################
       env.update({
          "CK_AR": "$#tool_prefix#$ar", 
          "CK_ASM_EXT": ".s", 
          "CK_CC": "$#tool_prefix#$clang$#tool_postfix#$", 
          "CK_LLVM_CONFIG": "$#tool_prefix#$llvm-config$#tool_postfix#$", 
          "CK_COMPILER_FLAGS_OBLIGATORY": "", 
          "CK_COMPILER_ENABLE_EXCEPTIONS": "-fcxx-exceptions",
          "CK_COMPILER_FLAG_CPP17": "-std=c++17",
          "CK_COMPILER_FLAG_CPP14": "-std=c++14",
          "CK_COMPILER_FLAG_CPP11": "-std=c++11", 
          "CK_COMPILER_FLAG_CPP0X": "-std=c++0x", 
          "CK_COMPILER_FLAG_GPROF": "-pg", 
          "CK_COMPILER_FLAG_OPENMP": "-fopenmp", 
          "CK_COMPILER_FLAG_PLUGIN": "-fplugin=", 
          "CK_COMPILER_FLAG_PTHREAD_LIB": "-lpthread", 
          "CK_CXX": "$#tool_prefix#$clang++$#tool_postfix#$", 
          "CK_DLL_EXT": ".so", 
          "CK_EXE_EXT": ".out", 
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
          "CK_LD_FLAGS_EXTRA": "", 
          "CK_LIB_EXT": ".a", 
          "CK_LINKER_FLAG_OPENMP": "-fopenmp", 
          "CK_MAKE": "make", 
          "CK_OBJDUMP": "$#tool_prefix#$objdump -d", 
          "CK_OBJ_EXT": ".o", 
          "CK_OPT_SIZE": "-Os", 
          "CK_OPT_SPEED": "-O3", 
          "CK_OPT_SPEED_SAFE": "-O2", 
          "CK_PLUGIN_FLAG": "-fplugin=", 
          "CK_PROFILER": "gprof"
        })

       # Modify if Android
       if remote=='yes':
          env.update({
             "CK_AR": "${CK_ANDROID_COMPILER_PREFIX}-ar", 
             "CK_COMPILER_FLAG_GPROF": "-pg", 
             "CK_DLL_EXT": ".so", 
             "CK_EXE_EXT": ".out", 
             "CK_EXTRA_LIB_DL": "-ldl", 
             "CK_EXTRA_LIB_M": "-lm", 
             "CK_FLAGS_DLL": "-shared -fPIC", 
             "CK_FLAGS_DLL_EXTRA": "", 
             "CK_FLAGS_STATIC_BIN": "-static -fPIC", 
             "CK_FLAGS_STATIC_LIB": "-fPIC", 
             "CK_LB": "${CK_ANDROID_COMPILER_PREFIX}-ar rcs", 
             "CK_LB_OUTPUT": "-o ", 
             "CK_LD_FLAGS_EXTRA": "", 
             "CK_LIB_EXT": ".a", 
             "CK_LD_DYNAMIC_FLAGS": "", 
             "CK_LD_FLAGS_EXTRA": "", 
             "CK_OBJDUMP": "${CK_ANDROID_COMPILER_PREFIX}-objdump -d",
             "CK_PROFILER": "gprof"})
       elif macos=='yes':
          env["CK_LB"]="$#tool_prefix#$ar -rcs"
          env["CK_LB_OUTPUT"]=""
       else:
          env["CK_LB"]="$#tool_prefix#$ar rcs"
          env["CK_LB_OUTPUT"]="-o "

       # Ask a few more questions
       # (tool prefix)
       prefix_configured=cus.get('tool_prefix_configured','')
       prefix=cus.get('tool_prefix','')

       env['CK_COMPILER_PREFIX']=prefix
       cus['tool_prefix']=prefix
       cus['tool_prefix_configured']='yes'

       for k in env:
           v=env[k]
           v=v.replace('$#tool_prefix#$',prefix)
           env[k]=v

       # (tool postfix such as -3.6)
       postfix_configured=cus.get('tool_postfix_configured','')
       postfix=cus.get('tool_postfix','')

       if postfix_configured!='yes':
          ck.out('')
          ra=ck.inp({'text':'Input clang postfix if needed (for example, -3.6 for clang-3.6) or Enter to skip: '})
          postfix=ra['string'].strip()

       env['CK_COMPILER_POSTFIX']=postfix
       cus['tool_postfix']=postfix
       cus['tool_postfix_configured']='yes'

       for k in env:
           v=env[k]

           # Hack to check that sometimes clang++-3.x is not available
           if k=='CK_CXX':
               pxx=os.path.join(env.get(ep+'_BIN',''),v.replace('$#tool_postfix#$',postfix))
               if not os.path.isfile(pxx):
                   v=v.replace('$#tool_postfix#$','')

           v=v.replace('$#tool_postfix#$',postfix)
           env[k]=v

       retarget=cus.get('retarget','')
       lfr=cus.get('linking_for_retargeting','')

       if retarget=='yes' and lfr!='':
          cus['linking_for_retargeting']=lfr
          env['CK_LD_FLAGS_EXTRA']=lfr

       if remote=='yes':
          ### Android target #########################################################

#          x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
          y='-target $CK_ANDROID_TOOLCHAIN -gcc-toolchain $CK_ENV_COMPILER_GCC --sysroot=$CK_SYS_ROOT'

          x=''
#          if arch=='arm64': 
#             x='-fPIE -pie '
          x='-fPIE -pie '

          env["CK_COMPILER_FLAGS_OBLIGATORY"]=' '+x+y

       else:
          ### Linux Host  #########################################################
          add_m32=cus.get('add_m32','')
          if add_m32=='' and iv=='yes' and tbits=='32':
             ra=ck.inp({'text':'Target OS is 32 bit. Add -m32 to compilation flags (y/N)? '})
             x=ra['string'].strip().lower()
             if x=='y' or x=='yes': 
                add_m32='yes'
                cus['add_m32']='yes'

          x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
          if tbits=='32' and add_m32=='yes' and x.find('-m32')<0: 
             x+=' -m32' 

          y=cus.get('add_to_ck_compiler_flags_obligatory','')
          if y!='' and x.find(y)<0:
             x+=' '+y
          env['CK_COMPILER_FLAGS_OBLIGATORY']=x

       x=cus.get('add_extra_path','')
       if x!='':
          s+='\nexport PATH='+pi+x+':%PATH%\n\n'

    # Starting from NDK v16 there is no more usr/include path under platform dir,
    # so we have to add it as explicit -Isysroot/usr/include under ndk root dir.

    sysroot_include_dir = os.path.join(ndk_path, 'sysroot', 'usr', 'include')
    env['CK_ENV_LIB_SYSROOT_INCLUDE']=sysroot_include_dir

    # Trying to form a correct ORDER of include directories to satisfy the #include_next mechanism:
    #
    env['CK_COMPILER_FLAGS_OBLIGATORY'] += ' -I'+env['CK_ENV_LIB_STDCPP_INCLUDE']+' -I'+env['CK_ENV_LIB_SYSROOT_INCLUDE']
    if os.path.isdir(sysroot_include_dir):
        asm_include_dirs = {
            'arm64': 'aarch64-linux-android',
            'arm': 'arm-linux-androideabi',
            'x86_64': 'x86_64-linux-android',
            'x86': 'i686-linux-android',
            'mips': 'mipsel-linux-android',
            'mips64': 'mips64el-linux-android',
        }
        if arch in asm_include_dirs:
            env['CK_COMPILER_FLAGS_OBLIGATORY'] += ' -I' + os.path.join(sysroot_include_dir, asm_include_dirs[arch])

    # Update global
    env['CK_COMPILER_TOOLCHAIN_NAME']='clang'

    env["CK_EXTRA_LIB_ATOMIC"]="-latomic"
    env['CK_HAS_OPENMP']='0' # for now force not to use OpenMP - later should detect via version

    if remote=='yes' or os_name_long.find('-arm')>0:
       y='-mfloat-abi=hard'
       env.update({'CK_COMPILER_FLAG_MFLOAT_ABI_HARD': y})

#       x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
#       if y not in x:
#          x+=' '+y
#          env["CK_COMPILER_FLAGS_OBLIGATORY"]=x

    # Otherwise may be problems on Windows during cross-compiling
    env['CK_OPT_UNWIND']=' '
    env['CK_FLAGS_DYNAMIC_BIN']=' '

    return {'return':0, 'bat':s}
