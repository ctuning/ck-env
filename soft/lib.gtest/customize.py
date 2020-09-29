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

    s=''

    cus=i.get('customize',{})
    full_path=cus.get('full_path','')
    hosd=i['host_os_dict']

    env=i['env']
    ep=cus['env_prefix']

    pi=os.path.dirname(full_path)
    while True:
        if os.path.isdir(os.path.join(pi,'lib')):
            found=True
            break
        pix=os.path.dirname(pi)
        if pix==pi:
            found=False
            break
        pi=pix

    if not found:
        return {'return':1, 'error':'can\'t find root dir of this installation'}

    cus['path_lib']         = os.path.join(pi,'lib')
    cus['path_include']     = os.path.join(pi,'include')

    r = ck.access({'action': 'lib_path_export_script', 
                   'module_uoa': 'os', 
                   'host_os_dict': hosd, 
                   'lib_path': cus.get('path_lib', '')})
    if r['return']>0: return r
    s += r['script']

    static_lib_name         = 'libgtest.a'

    cus['static_lib']       = static_lib_name
    env[ep+'_STATIC_NAME']  = static_lib_name
    env[ep]                 = pi

    return {'return':0, 'bat':s}
