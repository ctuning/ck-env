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

    hosd            = i['host_os_dict']
    tosd            = i['target_os_dict']
    winh            = hosd.get('windows_base','')

    toolchain_name  = tosd['android_toolchain']

    path_tc_root    = full_path if os.path.isdir(full_path) else os.path.dirname(full_path)     # 'install/'
    path_tools      = os.path.join(path_tc_root, toolchain_name, 'bin') # readelf etc
    path_lib        = os.path.join(path_tc_root, toolchain_name, 'lib') # libc++_shared.so or libgnustl_shared.so
    path_bin        = os.path.join(path_tc_root, 'bin')
    path_include    = os.path.join(path_tc_root, 'include')

    env                         = i.get('env', {})
    env[env_prefix]             = os.path.dirname(path_tc_root)
    env[env_prefix + '_ROOT']   = path_tc_root
    env[env_prefix + '_TOOLS']  = path_tools
    cus['path_lib']             = path_lib
    cus['path_bin']             = path_bin
    cus['path_include']         = path_include

    if winh=='yes':
        shell_script    = '\nset PATH=' + ';'.join([path_bin, '%PATH%']) + '\n\n'
    else:
        shell_script    = '\nexport PATH=' + ':'.join([path_bin, '$PATH']) + '\n\n'

    ## Prepend the hidden variables with env_prefix
    #
    for varname in install_env.keys():
        if varname.startswith('_'):
            env[env_prefix + varname] = install_env[varname]

    return {'return':0, 'bat':shell_script}

