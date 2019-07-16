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
        win_dir = 'C:\\MinGW'
        if os.path.isdir(win_dir):
            dirs.append(win_dir)
    return {'return':0, 'dirs':dirs}

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

        if q.find('X11')>0 or q.find('/lib/')>0 or q.endswith('.bz2') or \
           q.endswith('.ebuild') or q.endswith('.gz') or q.find('completion')>0:
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

    # Get variables
    ck=i['ck_kernel']

    iv=i.get('interactive','')

    env=i['env']
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})
    tags=i.get('tags',[])
    cus=i['customize']

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    hplat=hosd.get('ck_name','')

    target_d=i.get('target_os_dict',{})
    winh=hosd.get('windows_base','')
    win=target_d.get('windows_base','')
    mac=target_d.get('macos','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    file_extensions = target_d.get('file_extensions',{})

    envp=cus.get('env_prefix','')
    path_install=cus.get('path_install','')

    full_path=cus.get('full_path','')

    # Check path
    ep=cus.get('env_prefix','')
    if full_path!='':

       path_bin=os.path.dirname(full_path)
       path_install=os.path.dirname(path_bin)

       # Ask the compiler where it keeps its dynamic library -
       # it may be used by other components and should be exposed:

       first_param = '-print-file-name=libstdc++' + file_extensions.get('dll','')
       path_lib=''

       r=ck.access({'action':'run_and_get_stdout',
                    'module_uoa':'os',
                    'cmd': full_path+' '+first_param})
       if r['return']>0:
          ck.out('WARNING: problem obtaining GCC LIB path ('+r['error']+')')
       else:
          xpath_lib=r['stdout'].strip()
          if xpath_lib!='' and winh=='yes':
             xpath_lib=os.path.join(path_install,xpath_lib)

          # Check that file really exists
          if not os.path.isfile(xpath_lib):
             xpath_lib=''
          else:
             path_lib=os.path.dirname(xpath_lib)

       if path_lib=='':
          ck.out('WARNING: couldn\'t detect GCC stdlib++ path ...')


       if path_bin!='/usr/bin':
          cus['path_bin']=path_bin

       if ep!='':
          env[ep]           = path_install
          if path_bin!='/usr/bin':
              env[ep + '_BIN']  = path_bin
          if path_lib!='':
              env[ep + '_LIB']  = path_lib

       tool_postfix=''

       # Trick to check that long name
       pname=os.path.basename(full_path)

       j=pname.find('-gcc')
       if j>0:
          cus['tool_prefix']=pname[:j+1]

       if hplat=='linux':
          sname=cus.get('soft_file',{}).get(hplat,'')
          if pname.startswith(sname+'-'):
             tool_postfix=pname[len(sname):]

       if cus.get('tool_prefix','')=='':
          cus['tool_prefix_configured']='yes'
          cus['tool_prefix']=''
       if cus.get('tool_postfix','')=='':
          cus['tool_postfix_configured']='yes'
          cus['tool_postfix']=tool_postfix
       if cus.get('retarget','')=='':
          cus['retarget']='no'

    env.update({
      "CK_AR": "$#tool_prefix#$ar", 
      "CK_RANLIB": "$#tool_prefix#$ranlib", 
      "CK_ASM_EXT": ".s", 
      "CK_CC": "$#tool_prefix#$gcc$#tool_postfix#$",
      "CK_CC_FULL_PATH": os.path.join(path_bin, "$#tool_prefix#$gcc$#tool_postfix#$"),
      "CK_COMPILER_FLAGS_OBLIGATORY": "", 
      "CK_COMPILER_FLAG_CPP1Z": "-std=c++1z", 
      "CK_COMPILER_FLAG_CPP14": "-std=c++14", 
      "CK_COMPILER_FLAG_CPP11": "-std=c++11", 
      "CK_COMPILER_FLAG_CPP0X": "-std=c++0x", 
      "CK_COMPILER_FLAG_STD90": "-std=c90", 
      "CK_COMPILER_FLAG_STD99": "-std=c99", 
      "CK_COMPILER_FLAG_STD_GNU89": "-std=gnu89", 
      "CK_COMPILER_FLAG_GPROF": "-pg", 
      "CK_COMPILER_FLAG_OPENMP": "-fopenmp", 
      "CK_COMPILER_FLAG_PLUGIN": "-fplugin=", 
      "CK_COMPILER_FLAG_PTHREAD_LIB": "-lpthread", 
      "CK_COMPILER_TOOLCHAIN_NAME": "gcc",
      "CK_COMPILER_VERSION": i.get('version', ''),
      "CK_OPT_ALL_WARNINGS": "-Wall", 
      "CK_CXX": "$#tool_prefix#$g++$#tool_postfix#$",
      "CK_CXX_FULL_PATH": os.path.join(path_bin, "$#tool_prefix#$g++$#tool_postfix#$"),
      "CK_DLL_EXT": file_extensions.get('dll',''),
      "CK_EXE_EXT": file_extensions.get('exe',''),
      "CK_EXTRA_LIB_ATOMIC": "-latomic", 
      "CK_EXTRA_LIB_DL": "-ldl", 
      "CK_EXTRA_LIB_M": "-lm", 
      "CK_EXTRA_LIB_RT": "-lrt", 
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
      "CK_LB_OUTPUT": '' if mac=='yes' else '-o ',
      "CK_LD": "$#tool_prefix#$ld", 
      "CK_LD_FLAGS_EXTRA": "", 
      "CK_LIB_EXT": file_extensions.get('lib',''),
      "CK_LINKER_FLAG_OPENMP": "-lgomp -lrt", 
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
    prefix_configured=cus.get('tool_prefix_configured','')
    prefix=cus.get('tool_prefix','')
    if prefix_configured!='yes' and iv=='yes':
       if prefix!='':
          ck.out('Current compiler name prefix: '+prefix)
       else:
          ra=ck.inp({'text':'Compiler name prefix, if needed (such as "arm-none-linux-gnueabi-"): '})
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

    # (tool postfix such as -4.6)
    postfix_configured=cus.get('tool_postfix_configured','')
    postfix=cus.get('tool_postfix','')

    if postfix_configured!='yes':
       ra=ck.inp({'text':'Input gcc postfix if needed (for example, -4.6 for gcc-4.6) or Enter to skip: '})
       postfix=ra['string'].strip()

    env['CK_COMPILER_POSTFIX']=postfix
    cus['tool_postfix']=postfix
    cus['tool_postfix_configured']='yes'

    for k in env:
        v=env[k]
        v=v.replace('$#tool_postfix#$',postfix)
        env[k]=v

    retarget=cus.get('retarget','')
    lfr=cus.get('linking_for_retargeting','')
    if retarget=='' and iv=='yes':
       ra=ck.inp({'text':'Using retargeting (for example, for ARM) (y/N)? '})
       x=ra['string'].strip().lower()
       if x!='' and x=='y' or x=='yes':
          retarget='yes'
          cus['retarget']='yes'
          if 'retargeted' not in tags: tags.append('retargeted')

          if lfr=='' and iv=='yes':
#             y='-Wl,-dynamic-linker,/data/local/tmp/ld-linux.so.3 -Wl,--rpath -Wl,/data/local/tmp'
             ra=ck.inp({'text':'LD extra flags for retargeting (if needed): '})
             lfr=ra['string'].strip()
#             if lfr=='': lfr=y

       else:
          cus['retarget']='no'

    if retarget=='yes' and lfr!='':
       cus['linking_for_retargeting']=lfr
       env['CK_LD_FLAGS_EXTRA']=lfr

       env['CK_SYS_ROOT']=os.path.join(path_install, 'arm-none-linux-gnueabi', 'libc')

       x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
       y='--sysroot="'+env['CK_SYS_ROOT']+'"'
       if y not in x: 
          x+=y+' '
          env['CK_COMPILER_FLAGS_OBLIGATORY']=x

    add_m32=cus.get('add_m32','')
    if env.get('CK_COMPILER_ADD_M32','').lower()=='yes' or os.environ.get('CK_COMPILER_ADD_M32','').lower()=='yes':
       add_m32='yes'
       cus['add_m32']='yes'

#    if add_m32=='' and iv=='yes' and tbits=='32':
#       ra=ck.inp({'text':'Target OS is 32 bit. Add -m32 to compilation flags (y/N)? '})
#       x=ra['string'].strip().lower()
#       if x=='y' or x=='yes': 
#          add_m32='yes'
#          cus['add_m32']='yes'

    if winh=='yes':
       x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
       if remote!='yes':
          if x.find('-DWINDOWS')<0: 
             x+=' -DWINDOWS' 
       if tbits=='32' and add_m32=='yes' and x.find('-m32')<0: 
          x+=' -m32' 
       env['CK_COMPILER_FLAGS_OBLIGATORY']=x

       if mingw=='yes': env['CK_MAKE']='mingw32-make'
       elif remote=='yes': env['CK_MAKE']='cs-make'

       x=env.get('CK_CXX','')
       if x!='' and x.find('-fpermissive')<0:
          x+=' -fpermissive'
       env['CK_CXX']=x

       env['CK_CMAKE_GENERATOR']='MinGW Makefiles'

    #  Check some unusal GCC installations on Linux
    if winh!='yes':

       x=env.get('CK_AR','')
       x1=os.path.join(path_bin,x)
       if not os.path.isfile(x1):
          x='gcc-ar'
          x1=os.path.join(path_bin,x)
          if os.path.isfile(x1):
             env['CK_AR']=x
             env['CK_LB']=x+' rcs'

       x=env.get('CK_RANLIB','')
       x1=os.path.join(path_bin,x)
       if not os.path.isfile(x1):
          x='gcc-ranlib'
          x1=os.path.join(path_bin,x)
          if os.path.isfile(x1):
             env['CK_RANLIB']=x

    shell_setup_script_contents = ''

    x=cus.get('bugfix1','')
    if winh!='yes' and (x=='yes' or os.path.isdir('/usr/lib/x86_64-linux-gnu')):
       shell_setup_script_contents+='\nexport LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LIBRARY_PATH\n'

    x=cus.get('add_extra_path','')
    if x!='' and winh=='yes':
       shell_setup_script_contents+='\nset PATH='+path_install+x+';%PATH%\n\n'

    if mac=='yes':
        shell_setup_script_contents+='\nexport DYLD_LIBRARY_PATH={}:$DYLD_LIBRARY_PATH\n'.format(path_lib)

    # Otherwise may be problems on Windows during cross-compiling
    env['CK_OPT_UNWIND']=' '
    env['CK_FLAGS_DYNAMIC_BIN']=' '

    return {'return':0, 'bat':shell_setup_script_contents, 'env':env, 'tags':tags}
