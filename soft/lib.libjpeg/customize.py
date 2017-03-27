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

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    sdirs=hosd.get('dir_sep','')

    # Check platform
    hplat=hosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    win=tosd.get('windows_base','')
    mingw=tosd.get('mingw','')
    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    env=i['env']

    ep=cus['env_prefix']

    plib=os.path.dirname(fp)
    pi=os.path.dirname(plib)

    env[ep]=pi

    pname=os.path.basename(fp)
    j=pname.rfind('.')
    if j>0:
       pname=pname[:j]

    cus['path_lib']=plib
    cus['path_include']=pi+sdirs+'include'

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

    r = ck.access({'action': 'lib_path_export_script',
                   'module_uoa': 'os', 
                   'host_os_dict': hosd, 
                   'lib_path': cus.get('path_lib','')})
    if r['return']>0: return r
    s+=r['script']

    x=os.path.join(plib, pname+sext)
    if os.path.isfile(x):
       cus['static_lib']=pname+sext
       env[ep+'_STATIC_NAME']=pname+sext

    x=os.path.join(plib, pname+dext)
    if os.path.isfile(x):
       cus['dynamic_lib']=pname+dext
       env[ep+'_DYNAMIC_NAME']=pname+dext

    return {'return':0, 'bat':s}
