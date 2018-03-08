#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Leo Gordon @ dividiti
#

import os

##############################################################################
# get version from path

def version_cmd(i):

    full_path       = i['full_path']
    version_string  = ''

    if os.path.islink(full_path):
        symlink_target  = os.readlink(full_path)
        library_name    = os.path.basename(full_path)
        orig_length     = len(library_name)

        #       Linux style library version:
        if library_name == symlink_target[:orig_length] :
            version_string = symlink_target[orig_length+1:]
        else:
            (base, ext) = library_name.rsplit('.', 1)
            base_length = len(base)
            ext_length  = len(ext)

            #       OSX style library version:
            if base == symlink_target[:base_length] and ext == symlink_target[-ext_length:] :
                version_string = symlink_target[base_length+1:-ext_length-1]

    return {'return':0, 'cmd':'', 'version': version_string}

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

    # Get variables
    ck      = i['ck_kernel']
    cus     = i.get('customize',{})
    fp      = cus.get('full_path','')

    path_lib        = os.path.dirname( fp )
    install_root    = os.path.dirname( path_lib )
    while True:
       if os.path.isdir(os.path.join(install_root,'lib')):
          found=True
          break
       up_one_level = os.path.dirname(install_root)
       if up_one_level == install_root:
          found=False
          break
       install_root = up_one_level

    if not found:
       return {'return':1, 'error':'can\'t find root dir of this installation'}

    env                     = i['env']
    hosd                    = i['host_os_dict']
    tosd                    = i['target_os_dict']
    file_extensions         = hosd.get('file_extensions',{})    # not clear whether hosd or tosd should be used in soft detection
    file_root_name          = cus['file_root_name']
    static_lib_name         = file_root_name + file_extensions.get('lib','')
    dynamic_lib_name        = file_root_name + file_extensions.get('dll','')
    env_prefix              = cus['env_prefix']

    cus['path_lib']                 = path_lib
    cus['path_include']             = os.path.join(install_root,'include')
    cus['path_bin']                 = os.path.join(install_root,'bin')
    cus['static_lib']               = static_lib_name
    cus['dynamic_lib']              = dynamic_lib_name

    env[env_prefix]                 = install_root
    env[env_prefix+'_STATIC_NAME']  = static_lib_name
    env[env_prefix+'_DYNAMIC_NAME'] = dynamic_lib_name

    r = ck.access({'action': 'lib_path_export_script', 
                   'module_uoa': 'os', 
                   'host_os_dict': hosd, 
                   'lib_path': path_lib })
    if r['return']>0: return r
    shell_setup_script_contents = r['script']

    return {'return': 0, 'bat': shell_setup_script_contents}
