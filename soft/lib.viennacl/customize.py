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

    tosd=i.get('target_os_dict',{})
    win=tosd.get('windows_base','')
    remote=tosd.get('remote','')
    mingw=tosd.get('mingw','')
    tbits=tosd.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    hosd=i.get('host_os_dict',{})
    sdirs=hosd.get('dir_sep','')

    tplat=tosd.get('ck_name','')

    fp=cus.get('full_path','')

    p1=os.path.dirname(fp)
    pi=os.path.dirname(p1)

    pname=os.path.basename(fp)
    j=pname.rfind('.')
    if j>0:
       pname=pname[:j]

    plib=pi+sdirs+'lib'
    cus['path_lib']=plib
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

    r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': hosd, 
      'lib_path': cus.get('path_lib','')})
    if r['return']>0: return r
    s += r['script']

    cus['include_name']='viennacl.h'
    env[ep+'_INCLUDE_NAME']=cus.get('include_name','')

    # Prepare cache dir for kernels
    import tempfile
    dtmp=tempfile.gettempdir()

    cache_path='viennacl_cache'

    vcp=os.path.join(dtmp,cache_path)
    if not os.path.isdir(vcp): os.makedirs(vcp)

    # os.sep is needed at the end otherwise ViennaCL will not use it as a directory name, but as a file name ...
    vcp = vcp + os.sep
    env['VIENNACL_CACHE_PATH'] = vcp

    if tplat=='win':
      s += '\nmd "' + vcp + '"\n\n'
    else:
      s += '\nmkdir -p "' + vcp + '"\n\n'

    # If remote, also overwrite this env with remote device path
    # However do not forget that ViennaCL does not create directory for Cache,
    # so we need to have an existing dir ...
    if remote=='yes':
       dremote=tosd.get('remote_dir','')
       if dremote!='':
          tplat2=tosd.get('ck_name2','')

          if 'env_by_os' not in cus: cus['env_by_os']={}
          if tplat2 not in cus['env_by_os']: cus['env_by_os'][tplat2]={}
          cus['env_by_os'][tplat2]['VIENNACL_CACHE_PATH']=dremote+tosd.get('dir_sep','')+cache_path+'_'

    x=os.path.join(plib, pname+sext)
    if os.path.isfile(x):
       cus['static_lib']=pname+sext
       env[ep+'_STATIC_NAME']=pname+sext

    x=os.path.join(plib, pname+dext)
    if os.path.isfile(x):
       cus['dynamic_lib']=pname+dext
       env[ep+'_DYNAMIC_NAME']=pname+dext

    return {'return':0, 'bat':s}
