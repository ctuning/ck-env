#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
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

    # Get variables
    ck=i['ck_kernel']
    s=''

    iv=i.get('interactive','')

    env=i.get('env',{})
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})
    tags=i.get('tags',[])
    cus=i.get('customize',{})

    target_d=i.get('target_os_dict',{})
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')
    pb=cus.get('path_bin','')
    pl=cus.get('path_lib','')

    ck.out (cus)

    ################################################################
    pv='gcc-plugin-ici2'
    cus['ici_plugin_ver']=pv

    env['ICI2_PLUGIN_VER']=pv
    env['ICI_PLUGIN_VER']=pv
    env['ICI_LIB']=pl
    env['CCC_ICI_USE']='ICI_USE'
    env['CCC_ICI_PLUGINS']='ICI_PLUGIN'
    env['CCC_ICI_PASSES_FN']='ici_passes_function'
    env['CCC_ICI_PASSES_EXT']='.txt'
    env['CCC_ICI_PASSES_RECORD_PLUGIN']=os.path.join(pl, pv+'-extract-program-structure.so')
    env['CCC_ICI_FEATURES_ST_FN']='ici_features_function'
    env['CCC_ICI_FEATURES_ST_EXT']='.ft'
    env['CCC_ICI_FEATURES_ST_EXTRACT_PLUGIN']=os.path.join(pl, pv+'-extract-program-static-features.so')
    env['ICI_PROG_FEAT_PASS']='fre'
    env['ML_ST_FEAT_TOOL']=os.path.join(pb,'featlstn.P')
    env['ICI_PROG_FEAT_EXT_TOOL']=os.path.join(pb,'ml-feat-proc')

    return {'return':0, 'bat':s}
