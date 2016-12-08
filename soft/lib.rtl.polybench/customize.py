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

    target_d=i.get('target_os_dict',{})
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    host_d=i.get('host_os_dict',{})
    sdirs=host_d.get('dir_sep','')

    fp=cus.get('full_path','')
    if fp!='':
       p1=os.path.dirname(fp)
       pi=os.path.dirname(p1)

       cus['path_lib']=pi+sdirs+'lib'
       cus['path_include']=pi+sdirs+'include'

    ep=cus.get('env_prefix','')
    if ep!='':
       if pi!='':
          env[ep]=pi

    ################################################################
    if win=='yes':
       if remote=='yes' or mingw=='yes': 
          sext='.a'
          dext='.so'
       else:
          sext='.lib'
          dext='.dll'
    else:
       sext='.a'
       dext='.so'

    r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': host_d, 
      'lib_path': cus.get('path_lib', '')})
    if r['return']>0: return r
    s += r['script']

    cus['include_name']='polybench.h'
    cus['static_lib']='librtlpolybench'+sext
    cus['dynamic_lib']='librtlpolybench'+dext

    env['CK_ENV_LIB_RTL_POLYBENCH_INCLUDE_NAME']=cus.get('include_name','')
    env['CK_ENV_LIB_RTL_POLYBENCH_STATIC_NAME']=cus.get('static_lib','')
    env['CK_ENV_LIB_RTL_POLYBENCH_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    return {'return':0, 'bat':s}
