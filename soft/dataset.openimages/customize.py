#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
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

    sdirs=hosd.get('dir_sep','')

    # Check platform
    hplat=hosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    env=i['env']

    p1=os.path.dirname(fp)
    pi=os.path.dirname(p1)

    ep=cus.get('env_prefix','')

    ie = cus.get('install_env', '')

    val_dir = ie.get('VAL_DIR', '')
    env[ep + '_VAL_IMAGE_DIR'] = val_dir
    env['CK_ENV_DATASET_IMAGE_DIR'] = p1

    ann = ie.get('VAL_FILE','')
    env['CK_ENV_DATASET_ANNOTATIONS'] = os.path.join(pi, ann)

    classes = ie.get('CLASSES_FILE','')
    env['CK_ENV_DATASET_CLASSES'] = os.path.join(pi, classes)

    env['CK_ENV_DATASET_TYPE']='openimages'
    env[ep] = pi

    return {'return':0, 'bat':s}
