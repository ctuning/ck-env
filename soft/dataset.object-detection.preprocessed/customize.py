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
    from math import sqrt

    ck_kernel       = i.get('ck_kernel')
    cus             = i.get('customize',{})
    full_path       = cus.get('full_path','')
    env_prefix      = cus.get('env_prefix','')
    install_env     = cus.get('install_env', {})
    detection_mode  = len(install_env) == 0

    path_install    = full_path if os.path.isdir(full_path) else os.path.dirname(full_path)
    env             = i.get('env', {})
    env[env_prefix + '_DIR'] = path_install

    if detection_mode:
        preprocessed_ext    = cus.get("detect_preprocessed_ext")
        bytes_per_pixel     = cus.get("detect_bytes_per_pixel")
        file_index_name     = cus.get("detect_file_index_name")
        full_index_path     = os.path.join(path_install, file_index_name)

        if os.path.exists(full_index_path):
            r=ck_kernel.load_text_file({'text_file':full_index_path})
            if r['return']>0: return
            file_and_size_index = r['string'].split("\n")[:-1]
            file_index          = [ name_and_size.split(';')[0] for name_and_size in file_and_size_index ]
        else:
            return {'return':1, 'error':'Detection failed since original dimensions are missing from index file {}'.format(full_index_path)}

        install_env.update({
            '_NEW_EXTENSION':       preprocessed_ext,
            '_SUBSET_FOF':          file_index_name,
            '_SUBSET_OFFSET':       0,
            '_SUBSET_VOLUME':       len(file_index),
            '_INPUT_SQUARE_SIDE':   int(sqrt( os.path.getsize(os.path.join(path_install,file_index[0]))/float(bytes_per_pixel) )),
        })

    ## Prepend the hidden variables with env_prefix
    #
    for varname in install_env.keys():
        if varname.startswith('_'):
            env[env_prefix + varname] = install_env[varname]

    dataset_source_name = 'dataset-source'
    dataset_source_is_available = dataset_source_name in i.get('deps', {})

    def dep_env(dep, var): return i['deps'][dep]['dict']['env'].get(var)

    for varname in ['CK_ENV_DATASET_TYPE', 'CK_ENV_DATASET_ANNOTATIONS']:
        if dataset_source_is_available:
            env[varname] = dep_env('dataset-source', varname)
        else:
            r=ck.inp({'text':'Dependency "{}" is not available, please enter the value for variable {}: '.format(dataset_source_name, varname)})
            env[varname] = r['string'].strip()

    return {'return':0, 'bat':''}
