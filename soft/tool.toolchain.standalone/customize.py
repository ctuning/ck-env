#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Leo Gordon, leo@dividiti.com
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

    cus             = i.get('customize',{})
    full_path       = cus.get('full_path','')
    env_prefix      = cus.get('env_prefix','')
    install_env     = cus.get('install_env', {})

    path_tc_root    = full_path if os.path.isdir(full_path) else os.path.dirname(full_path)
    env             = i.get('env', {})
    env[env_prefix + '_ROOT'] = path_tc_root
    env[env_prefix] = os.path.dirname(path_tc_root)

    cus['path_lib']     = os.path.join(path_tc_root, 'lib')
    cus['path_bin']     = os.path.join(path_tc_root, 'bin')
    cus['path_include'] = os.path.join(path_tc_root, 'include')

    ## Prepend the hidden variables with env_prefix
    #
    for varname in install_env.keys():
        if varname.startswith('_'):
            env[env_prefix + varname] = install_env[varname]

    return {'return':0, 'bat':''}

