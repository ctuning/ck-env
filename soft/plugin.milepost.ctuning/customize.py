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
              cfg          - dict of the soft entry
              tags         - list of tags
              env          - environment
              deps         - dependencies

              interactive  - if 'yes', ask questions

              (customize)  - external params for possible customization:

                             target_arm - if 'yes', target ARM
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
              env          - updated environment
              deps         - updated dependencies
              tags         - updated tags

              path         - install path
            }

    """

    import os

    # Get variables
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

    print (cus)

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
