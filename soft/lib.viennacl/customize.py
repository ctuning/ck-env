#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE for licensing details
# See CK COPYRIGHT for copyright details
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

    p1=os.path.dirname(fp)
    pi=os.path.dirname(p1)

    cus['path_lib']=pi+sdirs+'lib'
    cus['path_include']=pi+sdirs+'include'

    ep=cus.get('env_prefix','')
    if pi!='' and ep!='':
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

    hplat=host_d.get('ck_name','')
    if hplat!='win':
       if cus.get('path_lib','')!='':
          s+='export LD_LIBRARY_PATH="'+cus['path_lib']+'":$LD_LIBRARY_PATH\n'
          s+='export LIBRARY_PATH="'+cus['path_lib']+'":$LIBRARY_PATH\n\n'

    cus['include_name']='viennacl.h'
    cus['static_lib']='libviennacl'+sext
    cus['dynamic_lib']='libviennacl'+dext

    env[ep+'_INCLUDE_NAME']=cus.get('include_name','')
    env[ep+'_STATIC_NAME']=cus.get('static_lib','')
    env[ep+'_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    return {'return':0, 'bat':s}
