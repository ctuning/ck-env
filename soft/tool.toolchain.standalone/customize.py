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

    path_install    = full_path if os.path.isdir(full_path) else os.path.dirname(full_path)
    env             = i.get('env', {})
    env[env_prefix + '_DIR'] = path_install

    ## Prepend the hidden variables with env_prefix
    #
    for varname in install_env.keys():
        if varname.startswith('_'):
            env[env_prefix + varname] = install_env[varname]

        if varname in ['_X86', '_X86_64', '_ARM', '_ARM64', '_MIPS', '_MIPS64']:
            env[env_prefix + varname + '_DIR'] = os.path.join(path_install, varname.lower()[1:])

    return {'return':0, 'bat':''}

