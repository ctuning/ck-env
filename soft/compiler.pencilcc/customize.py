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
    winh=host_d.get('windows_base','')
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    ep=cus.get('env_prefix','')

    fp=cus.get('full_path','')
    p1=os.path.dirname(fp)
    pi=os.path.dirname(p1)

    env[ep]=pi

    cus['path_bin']=os.path.join(pi,'bin')
    cus['path_lib']=os.path.join(pi,'lib')
    cus['path_include']=os.path.join(pi,'include')

    ############################################################
    # Ask a few more questions
    prefix=''

    env['PENCIL_COMPILER_EXTRA_OPTIONS']='--target=prl -D__PENCIL__ --opencl-include-file='+cus['path_include']+'/pencil_opencl.h'
    env['PENCIL_INCLUDE_DIR']=cus['path_include']

    env['PRL_LIB_DIR']=cus['path_lib']
    env['PRL_INCLUDE_DIR']=cus['path_include']

    r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': host_d, 
      'dynamic_lib_path': cus['path_lib']})
    if r['return']>0: return r
    s += r['script']

    s+='export PATH='+cus['path_bin']+':$PATH\n\n'

    return {'return':0, 'bat':s, 'env':env, 'tags':tags}
