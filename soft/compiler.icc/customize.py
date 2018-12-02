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
# internal: select extension
def get_ext(i):

    hproc=i.get('host_processor','')
    tproc=i.get('target_processor','')

    ext=''
    if tproc=='x64': 
       if hproc=='x86':
          ext='ia32_intel64'
       elif hproc=='x64':
          ext='intel64'
       else:
          return {'return':1, 'error':'this software is not supporting ARM yet'}
    elif tproc=='x86':
         ext='ia32'
    else:
         return {'return':1, 'error':'this software is not supporting ARM yet'}

    return {'return':0, 'ext':ext}


##############################################################################
# customize directories to automatically find and register software

def dirs(i):
    return {'return':0}

##############################################################################
# limit files/directories ...

def limit(i):

    dr=i.get('list',[])
    drx=[]

    for q in dr:

        if q.find('pkg_')<0:
           drx.append(q)

    return {'return':0, 'list':drx}

##############################################################################
# prepare env

def version_cmd(i):

    fp=i['full_path']

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']
    cmdx=i['cmd']

    o=i.get('out','')

    nout=hosd.get('no_output','')
    xnout=''
    if o!='con':
       xnout=nout

    eifsc=hosd.get('env_quotes_if_space_in_call','')

    if eifsc!='' and fp.find(' ')>=0 and not fp.startswith(eifsc):
       fp=eifsc+fp+eifsc

    hplat=hosd.get('ck_name','')

    # Check platform
    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    rx=get_ext({'host_processor':hproc, 'target_processor':tproc})
    if rx['return']>0: return rx
    ext=rx['ext']

    cmd=''

    if hplat=='win':
       if fp!='':
          cmd =xnout+'call '+fp+' '+ext+'\n'
       cmd+=xnout+'icl '+cmdx+'\n'
    else:
       if fp!='':
          cmd =xnout+'. '+fp+' '+ext+'\n'
       cmd+=xnout+'icc '+cmdx+'\n'

    return {'return':0, 'cmd':cmd}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    hosd=i.get('host_os_dict',{})
    hplat=hosd.get('ck_name','')

    ver=''

    for q in lst:
        q=q.strip()
        if q!='':
           if q.find('license has expired')>=0:
              ver='expired'
              break
           if hplat=='win':
              j=q.lower().find(' version ')
              if j>=0:
                 q=q[j+10:]
                 j=q.find(' ')
                 if j>=0:
                    ver=q[:j]
                    break
           else:
              j=q.lower().find(') ')
              if j>=0:
                 ver=q[j+2:]
                 j=ver.find(' ')
                 if j>=0:
                    ver=ver[:j]
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

    cus=i.get('customize',{})

    env=i['env']

    hos=i['host_os_uid']
    tos=i['host_os_uid']
    tdid=i['target_device_id']

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    hwin=hosd.get('windows_base','')

    ep=cus.get('env_prefix','')
    fp=cus.get('full_path','')
    if ep!='' and fp!='':
       pi=os.path.dirname(fp)
       env[ep]=pi

    if 'android' in tosd.get('tags',[]):
       return {'return':1, 'error':'this software is not supporting Android platform'}

    # Check platform
    hplat=hosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')
    macos=hosd.get('macos', '')
    file_extensions = tosd.get('file_extensions',{})

    rx=get_ext({'host_processor':hproc, 'target_processor':tproc})
    if rx['return']>0: return rx
    ext=rx['ext']

    env=i['env']

    env.update({
        # FIXME: check whether Boost also agrees to compile under windows+icc and extend to windows platform if so
        "CK_COMPILER_TOOLCHAIN_NAME" : 'intel-' + ('darwin' if macos else 'linux'),
        "CK_COMPILER_VERSION": i.get('version', ''),
        "CK_DLL_EXT": file_extensions.get('dll',''),
        "CK_EXE_EXT": file_extensions.get('exe',''),
        "CK_LIB_EXT": file_extensions.get('lib',''),
        "CK_OPT_SIZE": "-Os",
        "CK_OPT_SPEED": "-O3",
        "CK_OPT_SPEED_SAFE": "-O2",
    })

    ############################################################
    # Setting environment depending on the platform
    if hplat=='linux':
       env.update({
         "CK_AR": "xiar",
         "CK_ASM_EXT": ".s", 
         "CK_CC": "icc", 
         "CK_COMPILER_FLAGS_OBLIGATORY": "", 
         "CK_COMPILER_FLAG_CPP11": "-Qstd=c++11", 
         "CK_COMPILER_FLAG_CPP0X": "-Qstd=c++0x", 
         "CK_COMPILER_FLAG_GPROF": "-pg", 
         "CK_COMPILER_FLAG_OPENMP": "-openmp", 
         "CK_COMPILER_FLAG_PTHREAD_LIB": "-pthread", 
         "CK_COMPILER_FLAG_STD90": "-Qstd=c90", 
         "CK_COMPILER_FLAG_STD99": "-Qstd=c99", 
         "CK_CSTD99": "-Qstd=c99", 
         "CK_CXX": "icc", 
         "CK_EXTRA_LIB_DL": "-ldl", 
         "CK_EXTRA_LIB_M": "-lm", 
         "CK_F90": "ifort", 
         "CK_F95": "ifort", 
         "CK_FC": "ifort", 
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
         "CK_LB": "ar rcs", 
         "CK_LB_OUTPUT": "-o ", 
         "CK_LD": "xild",
         "CK_LD_FLAGS_EXTRA": "", 
         "CK_LINKER_FLAG_OPENMP": "-lpthread -liomp5", 
         "CK_MAKE": "make", 
         "CK_OBJDUMP": "objdump -d", 
         "CK_OBJ_EXT": ".o", 
         "CK_PLUGIN_FLAG": "-fplugin=", 
         "CK_PROFILER": "gprof"
       })

       ################################################################
       s+='\n'
       s+='# Setting Intel compiler environment\n'

       s+='. "'+fp+'" '+ext+'\n\n'

    else:
       env.update({
         "CK_AR": "lib", 
         "CK_ASM_EXT": ".asm", 
         "CK_CC": "icl", 
         "CK_COMPILER_FLAGS_OBLIGATORY": "/DWINDOWS /GS-", 
         "CK_COMPILER_FLAG_CPP11": "/Qstd=c++11", 
         "CK_COMPILER_FLAG_CPP0X": "/Qstd=c++0x", 
         "CK_COMPILER_FLAG_OPENMP": "/openmp", 
         "CK_COMPILER_FLAG_PTHREAD_LIB": "/pthread", 
         "CK_COMPILER_FLAG_STD90": "/Qstd=c90", 
         "CK_COMPILER_FLAG_STD99": "/Qstd=c99", 
         "CK_CSTD99": "/Qstd=c99", 
         "CK_CXX": "icl", 
         "CK_EXTRA_LIB_DL": "", 
         "CK_EXTRA_LIB_M": "", 
         "CK_F90": "ifort /fpp", 
         "CK_F95": "ifort /fpp", 
         "CK_FC": "ifort /fpp", 
         "CK_FLAGS_CREATE_ASM": "/Fa /c", 
         "CK_FLAGS_CREATE_OBJ": "/c", 
         "CK_FLAGS_DLL": "/MT /DWin /LD", # /FIwindows.h", 
         "CK_FLAGS_DLL_EXTRA": "/link /dll", 
         "CK_FLAGS_DYNAMIC_BIN": "/MD", 
         "CK_FLAGS_OUTPUT": "/Fe", 
         "CK_FLAGS_STATIC_BIN": "/MT", 
         "CK_FLAGS_STATIC_LIB": "/MD", 
         "CK_FLAG_PREFIX_INCLUDE": "/I", 
         "CK_FLAG_PREFIX_VAR": "/D", 
         "CK_LB": "lib", 
         "CK_LB_OUTPUT": "/OUT:", 
         "CK_LD_DYNAMIC_FLAGS": "/link /NODEFAULTLIB:LIBCMT", 
#         "CK_LD_FLAGS_EXTRA": "bufferoverflowU.lib", 
         "CK_MAKE": "nmake", 
         "CK_OBJDUMP": "dumpbin /disasm", 
         "CK_OBJ_EXT": ".obj"
       })

       ############################################################
       s+='\n'
       s+='rem Setting environment\n'

       s+='call "'+fp+'" '+ext+'\n\n'

    # Attempt to detect path to compiler
    if hwin=='yes':
       cmd=s+'where '+env['CK_CC']+'.exe'
    else:
       cmd=s+'which '+env['CK_CC']

    r=ck.access({'action':'shell',
                 'module_uoa':'os',
                 'host_os':hos,
                 'target_os':tos,
                 'device_id':tdid,
                 'cmd':cmd,
                 'split_to_list':'yes'})
    if r['return']>0: return r

    pcl=''
    for x in reversed(r['stdout_lst']):
        x=x.strip()
        if x!='':
           if os.path.isfile(x):
              pcl=x
           break

    if ep!='' and pcl!='':
       # Found compiler path (useful for CMAKE)
       bin_dir = os.path.dirname(pcl)

       env[ep+'_BIN']                   = bin_dir
       env['CK_CC_FULL_PATH']           = os.path.join(bin_dir, env['CK_CC'])
       env['CK_CXX_FULL_PATH']          = os.path.join(bin_dir, env['CK_CXX'])
       env['CK_AR_PATH_FOR_CMAKE']      = os.path.join(bin_dir, 'xiar')
       env['CK_LD_PATH_FOR_CMAKE']      = os.path.join(bin_dir, 'xild')
       env['CK_RANLIB_PATH_FOR_CMAKE']  = '/usr/bin/ranlib'

       ## FIXME: A more elegant and portable solution would be to create an executable ranlib wrapper around 'xiar'.
       ##        The current problem is that we do not have access to the entry_dir at this point.
       #
       # path_to_wrapper  = os.path.join(entry_dir, 'ranlib_wrapper')
       # wrapper_contents = "#!/bin/bash\n\nexec " + env['CK_AR_PATH_FOR_CMAKE'] + " s $@\n"
       # rx=ck.save_text_file({'text_file' : path_to_wrapper, 'string' : wrapper_contents})
       # if rx['return']>0: return rx
       # os.chmod(path_to_wrapper, 0o755)
       # env['CK_RANLIB_PATH_FOR_CMAKE'] = path_to_wrapper

       ck.out('')
       ck.out('  * Found compiler in '+pcl)

    return {'return':0, 'bat':s}
