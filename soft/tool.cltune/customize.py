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
    hosd=i['host_os_dict']
    target_d=i.get('target_os_dict',{})
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    fp=cus.get('full_path','')

    fn=os.path.basename(fp)

    pl=os.path.dirname(fp)
    pi=os.path.dirname(pl)
    ################################################################

    slib='libcltune.a'
    dlib='libcltune.so'

    xwin=False
    if win=='yes' and not (remote=='yes' or mingw=='yes'):
       slib='cltune.lib'
       dlib='cltune.dll'
       xwin=True

    if os.path.isfile(os.path.join(pl,slib)): 
       cus['static_lib']=slib
    if os.path.isfile(os.path.join(pl,dlib)): 
       cus['dynamic_lib']=dlib
       if xwin:
          s+='\nset PATH='+pl+';%PATH%\n'

    cus['dynamic_plugin']=fn
    env[envp+'_DYNAMIC_NAME']=cus['dynamic_plugin']
    env[envp+'_DYNAMIC_NAME_FULL']=fp
    env[envp]=pi
    env[envp+'_LIB']=pl
    cus['path_lib']=pl
    env[envp+'_INCLUDE']=pi+'/include/'
    r = ck.access({'action': 'lib_path_export_script', 
                   'module_uoa': 'os', 
                   'host_os_dict': hosd, 
                   'lib_path': cus.get('path_lib','')})
    if r['return']>0: return r

    s+=r['script']
  
    return {'return':0, 'bat':s}
