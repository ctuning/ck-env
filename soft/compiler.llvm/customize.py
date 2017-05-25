#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os

extra_dirs=['C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools',
            'D:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools']

sbin=[{"key":"CK_AR", "file":"llvm-ar", "extra":""},
      {"key":"CK_LB", "file":"llvm-ar", "extra":"rcs", "set_extra_key":"CK_LB_OUTPUT", "extra_value":"", "ignore_win":"yes"},
      {"key":"CK_OBJDUMP", "file":"llvm-objdump", "extra":"-d"},
      {"key":"CK_RANLIB", "file":"llvm-ranlib", "extra":""}]

##############################################################################
# customize directories to automatically find and register software

def dirs(i):
    hosd=i['host_os_dict']
    phosd=hosd.get('ck_name','')
    dirs=i.get('dirs', [])
    if phosd=='win':
        for d in extra_dirs:
            if os.path.isdir(d):
                dirs.append(d)
    return {'return':0}

##############################################################################
# limit files/directories ...

def limit(i):

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    sname=i['soft_name']

    phosd=hosd.get('ck_name','')

    dr=i.get('list',[])
    drx=[]

    for q in dr:
        add=True

        if q.find('X11')>0 or q.find('/lib/')>0:
           add=False

        if add and phosd=='linux':
           pq=os.path.basename(q)
           if len(pq)>len(sname) and pq[len(sname)]!='-':
              add=False

           if add and pq.startswith(sname+'-'):
              if len(pq)<=len(sname):
                 add=False
              else:
                 if not pq[len(sname)+1].isdigit():
                    add=False

        if add:
           drx.append(q)

    return {'return':0, 'list':drx}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip()
        if q!='':
           j=q.lower().find(' version ')
           if j>0 and q.lower().startswith('clang'):
              q=q[j+9:]
              j=q.find(' ')
              if j>0:
                 q=q[:j]
              ver=q
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

    hosd=i.get('host_os_dict',{})
    target_d=i.get('target_os_dict',{})
    winh=hosd.get('windows_base','')
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    sdirs=hosd.get('dir_sep','')

    mac=target_d.get('macos','')

    hplat=hosd.get('ck_name','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    fp=cus.get('full_path','')

    tp=''

    arch=target_d.get('android_ndk_arch','')

    # Check path
    ep=cus.get('env_prefix','')
    if ep!='' and fp!='':
       p1=os.path.dirname(fp)
       pi=os.path.dirname(p1)

       env[ep]=pi
       env[ep+'_BIN']=p1

       cus['path_lib']=pi+sdirs+'lib'
       cus['path_include']=pi+sdirs+'include'

       pname=os.path.basename(fp)

       j=pname.find('-clang')
       if j>0:
          cus['tool_prefix']=pname[:j+1]

       if hplat=='linux':
          sname=cus.get('soft_file',{}).get(hplat,'')
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


    env.update({"CK_COMPILER_FLAG_STD90": "-std=c90", 
                "CK_COMPILER_FLAG_STD99": "-std=c99"})

    ############################################################
    if winh=='yes':

       env.update({
             "CK_AFTER_COMPILE_TO_BC": "ren *.o *", 
             "CK_ASM_EXT": ".s", 
             "CK_BC_EXT": ".bc", 
             "CK_COMPILER_ENABLE_EXCEPTIONS": "-fcxx-exceptions",
             "CK_CC": "$#tool_prefix#$clang", 
             "CK_COMPILER_FLAG_CPP11": "-std=c++11", 
             "CK_COMPILER_FLAG_CPP0X": "-std=c++0x", 
             "CK_COMPILER_FLAG_OPENMP": "-fopenmp", 
             "CK_COMPILER_FLAG_PTHREAD_LIB": "-lpthread", 
             "CK_CXX": "$#tool_prefix#$clang++", 
             "CK_F90": "", 
             "CK_F95": "", 
             "CK_FC": "", 
             "CK_FLAGS_CREATE_ASM": "-S", 
             "CK_FLAGS_CREATE_BC": "-c -emit-llvm", 
             "CK_FLAGS_CREATE_OBJ": "-c", 
             "CK_FLAGS_DYNAMIC_BIN": " ", 
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
             "CK_FLAGS_STATIC_LIB": " ",  #-fPIC ???
             "CK_LB": "lib", 
             "CK_LB_OUTPUT": "/OUT:", 
             "CK_LD_DYNAMIC_FLAGS": "", 
             "CK_LD_FLAGS_MISC": "-fuse-ld=link.exe", 
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
          if arch=='arm64': 
             x='-fPIE -pie '

          env["CK_COMPILER_FLAGS_OBLIGATORY"]='-lm '+x+y
       else:
          env["CK_COMPILER_FLAGS_OBLIGATORY"]="-DWINDOWS"

          if retarget=='yes' and lfr!='':
             cus['linking_for_retargeting']=lfr
             env['CK_LD_FLAGS_EXTRA']=lfr

             add_m32=cus.get('add_m32','')
             if add_m32=='' and iv=='yes' and tbits=='32':
                ra=ck.inp({'text':'Target OS is 32 bit. Add -m32 to compilation flags (y/N)? '})
                x=ra['string'].strip().lower()
                if x=='y' or x=='yes': 
                   add_m32='yes'
                   cus['add_m32']='yes'

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
          "CK_COMPILER_FLAGS_OBLIGATORY": "", 
          "CK_COMPILER_ENABLE_EXCEPTIONS": "-fcxx-exceptions",
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
       elif mac=='yes':
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
          if arch=='arm64': 
             x='-fPIE -pie '

          env["CK_COMPILER_FLAGS_OBLIGATORY"]='-lm '+x+y

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

    env['CK_COMPILER_TOOLCHAIN_NAME']='clang'

    # CHECK if some LLVM specific binaries exist (rather than standard)
    for x in sbin:
        xk=x['key']
        xf=x['file']
        xe=x.get('extra','')

        xf1=x['file']
        if winh=='yes': 
           if x.get("ignore_win","")=="yes":
              continue
           xf1+='.exe'

        xp=os.path.join(p1,xf1)
        if os.path.isfile(xp):
           env[xk]=xf
           if xe!='': env[xk]+=' '+xe

           ek=x.get('set_extra_key','')
           if ek!='':
              env[ek]=x.get('extra_value','')

    # Update global
    if remote=='yes' or os_name_long.find('-arm')>0:
       y='-mfloat-abi=hard'
       env.update({'CK_COMPILER_FLAG_MFLOAT_ABI_HARD': y})

       x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
       if y not in x:
          x+=' '+y
          env["CK_COMPILER_FLAGS_OBLIGATORY"]=x

    # Otherwise may be problems on Windows during cross-compiling
    env['CK_OPT_UNWIND']=' '
    env['CK_FLAGS_DYNAMIC_BIN']=' '

    return {'return':0, 'bat':s}
