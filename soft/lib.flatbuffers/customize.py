#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Leo Gordon @ dividiti
#

import os


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

    # Get variables
    ck              = i['ck_kernel']
    cus             = i.get('customize',{})
    fp              = cus.get('full_path','')

    path_lib        = os.path.dirname( fp )
    install_root    = os.path.dirname( path_lib )
    path_include    = os.path.join( install_root, 'include' )
    path_bin        = os.path.join( install_root, 'bin' )

    env                         = i['env']
    hosd                        = i['host_os_dict']
    tosd                        = i['target_os_dict']
    file_extensions             = hosd.get('file_extensions',{})    # not clear whether hosd or tosd should be used in soft detection
    file_root_name              = cus['file_root_name']
    env_prefix                  = cus['env_prefix']

    cus['path_bin']             = path_bin
    cus['path_lib']             = path_lib
    cus['path_include']         = path_include

    env[env_prefix]             = install_root
    env[env_prefix+'_BIN']      = path_bin
    env[env_prefix+'_LIB']      = path_lib
    env[env_prefix+'_INCLUDE']  = path_include
    env[env_prefix+'_LFLAG']    = '-lflatbuffers'

    r = ck.access({'action': 'lib_path_export_script', 
                   'module_uoa': 'os', 
                   'host_os_dict': hosd, 
                   'lib_path': path_lib })
    if r['return']>0: return r
    shell_setup_script_contents = r['script']

    return {'return': 0, 'bat': shell_setup_script_contents}
