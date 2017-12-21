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
    fp=cus.get('full_path','')

    p0=os.path.basename(fp)
    p1=os.path.dirname(fp)
    pi=os.path.dirname(p1)
    pii=os.path.dirname(pi)

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    # Check platform
    hplat=hosd.get('ck_name','')
    win=tosd.get('windows_base','')
    mingw=tosd.get('mingw','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    env=i['env']

    found=False
    while True:
       if os.path.isdir(os.path.join(pi,'lib')):
          found=True
          break
       pix=os.path.dirname(pi)
       if pix==pi:
          break
       pi=pix

    if not found:
       return {'return':1, 'error':'can\'t find root dir of this installation'}

    ep=cus['env_prefix']
    env[ep]=pi

    ############################################################
    cus['path_lib']=p1
    cus['path_include']=os.path.join(pi,'include')
    cus['path_bin']=os.path.join(pi,'bin')

    r = ck.access({'action': 'lib_path_export_script', 
                   'module_uoa': 'os', 
                   'host_os_dict': hosd, 
                   'lib_path': cus.get('path_lib', '')})
    if r['return']>0: return r
    s += r['script']

    if win=='yes':
       if remote=='yes' or mingw=='yes': 
          ls='libxml2.a'
          ld='libxml2.so'
       else:
          ls='libxml2.lib'
          ld='libxml2.dll'
    else:
       ls='libxml2.a'
       ld='libxml2.so'

    cus['static_lib']=ls
    cus['dynamic_lib']=ld

    env[ep+'_STATIC_NAME']=cus.get('static_lib','')
    env[ep+'_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    if win!='yes':
       env[ep+'_LFLAG']='-lprotobuf'

    src=cus.get('install_env',{}).get('PACKAGE_SUB_DIR','')
    psrc=os.path.join(pii,src)

    if os.path.isdir(psrc):
       env[ep+'_SRC_DIR']=psrc

    return {'return':0, 'bat':s}
