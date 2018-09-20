#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Flavio Vella, flavio@dividiti.com
# OSX port:  Leo Gordon, leo@dividiti.com
#

import os

##############################################################################
# get version from path

def version_cmd(i):

    ck=i['ck_kernel']

    full_path=i['full_path']
    fn=os.path.basename(full_path)

    rfp=os.path.realpath(full_path)
    rfn=os.path.basename(rfp)

    ver=''

    if rfn.startswith(fn):
       ver=rfn[len(fn)+1:]
       if ver!='':
          ver='api-'+ver

    return {'return':0, 'cmd':'', 'version':ver}

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
    cus=i.get('customize',{})
    full_path=cus.get('full_path','')

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    # Check platform
    tplat=hosd.get('ck_name','')

    env=i['env']

    # Looking for the parent of the 'lib'/'lib64' dir:
    #
    path_lib        = os.path.dirname(full_path)
    lib_parent_dir  = path_lib
    found=False
    while True:
       if os.path.isdir(os.path.join(lib_parent_dir,'lib')) or os.path.isdir(os.path.join(lib_parent_dir,'lib64')):
          found=True
          break
       up_one_level=os.path.dirname(lib_parent_dir)
       if up_one_level==lib_parent_dir:
          break
       lib_parent_dir=up_one_level

    if not found:
       return {'return':1, 'error':'can\'t find root dir of the libBLAS installation'}


    # Looking for the parent of the 'include' dir that contains our include_file:
    #
    pl0 = os.path.dirname( os.path.realpath(full_path) )
    pl1 = os.path.dirname( pl0 )
    pl2 = os.path.dirname( pl1 )
    pl3 = os.path.dirname( pl2 )

    include_file_name=cus.get('include_file','')
    if os.path.isfile(os.path.join(pl0,'Headers',include_file_name)):
        include_parent_dir   = pl0
        include_sub_dir      = 'Headers'
    elif os.path.isfile(os.path.join(pl1,'include',include_file_name)):
        include_parent_dir   = pl1
        include_sub_dir      = 'include'
    elif os.path.isfile(os.path.join(pl2,'include',include_file_name)):
        include_parent_dir   = pl2
        include_sub_dir      = 'include'
    elif os.path.isfile(os.path.join(pl3,'include',include_file_name)):
        include_parent_dir   = pl3
        include_sub_dir      = 'include'
    elif os.path.isfile(os.path.join(pl3,'include','x86_64-linux-gnu',include_file_name)):
        include_parent_dir   = pl3
        include_sub_dir      = os.path.join(pl3,'include','x86_64-linux-gnu')
    elif os.path.isfile(os.path.join(pl3,'include','arm-linux-gnueabihf',include_file_name)):
        include_parent_dir   = pl3
        include_sub_dir      = os.path.join(pl3,'include','arm-linux-gnueabihf')
    else:
        return {'return':1, 'error':'can\'t find include file'}

    file_extensions     = hosd.get('file_extensions',{})    # not clear whether hosd or tosd should be used in soft detection
    file_root_name      = cus['file_root_name']
    cus['path_lib']     = path_lib
    cus['static_lib']   = file_root_name + file_extensions.get('lib','')
    cus['dynamic_lib']  = file_root_name + file_extensions.get('dll','')
    cus['path_include'] = os.path.join(include_parent_dir, include_sub_dir)
    cus['include_name'] = include_file_name

    r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': hosd, 'lib_path': path_lib})
    if r['return']>0: return r
    shell_setup_script_contents = r['script']

    env_prefix          = cus.get('env_prefix','')
    install_root        = include_parent_dir    # or should lib_parent_dir be used instead? Not clear.
    env[env_prefix]     = install_root

    path_bin=os.path.join(install_root,'bin')
    if os.path.isdir(path_bin):
       env[env_prefix+'_BIN']=path_bin
       cus['path_bin']=path_bin
       if tplat=='win':
          shell_setup_script_contents += '\nset PATH='+path_bin+';%PATH%\n\n'

    env[env_prefix+'_INCLUDE_NAME'] = cus.get('include_name','')
    env[env_prefix+'_STATIC_NAME']  = cus.get('static_lib','')
    env[env_prefix+'_DYNAMIC_NAME'] = cus.get('dynamic_lib','')

    return {'return':0, 'bat':shell_setup_script_contents}

