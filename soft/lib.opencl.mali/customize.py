#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

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

    host_d=i.get('host_os_dict',{})
    target_d=i.get('target_os_dict',{})
    win=target_d.get('windows_base','')
    winh=host_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    ################################################################
    cus['include_name']='CL/opencl.h'

    pl=os.path.join(pi,'lib')

    if remote=='yes': # Libraries are on remote device, use stubs
      cus['static_lib']='libOpenCL.so'
      cus['dynamic_lib']='libOpenCL.so'
    else:
      cus['static_lib']='libmali.so'
      cus['dynamic_lib']='libmali.so'

      if not os.path.isfile(os.path.join(pl,cus['dynamic_lib'])):
         return {'return':1, 'error':'libmali.so is not in lib directory - please copy driver libs there'}

    env['CK_ENV_LIB_OPENCL_INCLUDE_NAME']=cus.get('include_name','')
    env['CK_ENV_LIB_OPENCL_STATIC_NAME']=cus.get('static_lib','')
    env['CK_ENV_LIB_OPENCL_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    if remote=='yes':
       ck.out('')
       ck.out('Trying to compile OpenCL stubs lib ...')

       make=deps['compiler'].get('dict',{}).get('env',{}).get('CK_MAKE','')
       if make=='': make='make'

       if winh=='yes':
          x='CC="%CK_CXX% %CK_COMPILER_FLAGS_OBLIGATORY%"'
       else:
          x='CC="$CK_CXX $CK_COMPILER_FLAGS_OBLIGATORY"'

       # Prepare tmp script to run
       cmd=host_d.get('batch_prefix','')+'\n'
       cmd+=host_d['change_dir']+' '+pl+'\n'
       cmd+=deps['compiler']['bat'].strip()+'\n'
       cmd+=make+' '+x+'\n'

       ck.out ('******************')
       ck.out (cmd)
       ck.out ('******************')

       fscript='tmp-script'+host_d['script_ext']
       fx=open(fscript, 'w')
       fx.write(cmd)
       fx.close()

       scall=host_d.get('env_call','')
       sexe=host_d.get('set_executable','')
       envsep=host_d.get('env_separator','')

       y=''
       if sexe!='':
          y+=sexe+' '+fscript+envsep
       y+=' '+scall+' '+host_d.get('bin_prefix','')+fscript

       ck.out('')
       ck.out(' Executing "'+y+'"')

       rx=os.system(y)

       os.remove(fscript)

       if rx>0:
          ck.out ('')
          ck.out ('Possible Error: script returned non-zero code ('+str(rx)+') ...')

    return {'return':0, 'bat':s}
