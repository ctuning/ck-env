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

    # Check platform
    env=i['env']

    ep=cus['env_prefix']

    pl=os.path.dirname(fp)
    p2=os.path.dirname(pl)

    pb=os.path.join(p2,'bin')
    pinc=os.path.join(p2,'include')

    cus['path_bin']=pb
    cus['path_lib']=pl
    cus['path_include']=pinc

    env[ep]=p2
    env[ep+'_BIN']=pb
    env[ep+'_LIB']=pl
    env[ep+'_INCLUDE']=pinc

    lb=os.path.basename(fp)
    lbs=lb
    if lbs.endswith('.so'):
       lbs=lbs[:-3]+'.a'

    cus['static_lib']=lbs
    cus['dynamic_lib']=lb

    env[ep+'_STATIC_NAME']=cus.get('static_lib','')
    env[ep+'_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': hosd, 
      'lib_path': cus.get('path_lib','')})
    if r['return']>0: return r
    s += r['script']

    return {'return':0, 'bat':s}
