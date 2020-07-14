#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer(s):
# - Gavin Simpson, gavin.s.simpson@gmail.com
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

    winh=hosd.get('windows_base','')

    env=i['env']
    ep=cus['env_prefix']
    env[ep+'_VERSION']     = cus['install_env'].get('PACKAGE_VERSION','')
    env[ep+'_IE_PATH']     = fp
    env[ep+'_IE_NAME']     = os.path.basename(fp)
    lib_dir                = os.path.dirname(fp)
    install_dir            = os.path.dirname(lib_dir)
    env[ep]                = install_dir
    env[ep+'_BIN_DIR']     = os.path.join(install_dir, 'bin')
    env[ep+'_LIB_DIR']     = os.path.join(install_dir, 'lib')
    env[ep+'_INCLUDE_DIR'] = os.path.join(install_dir, 'include')
    env[ep+'_OBJ_DIR']     = os.path.join(install_dir, 'obj')

    return {'return':0, 'bat':s}
