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
    host_d=i.get('host_os_dict',{})
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    sdirs=host_d.get('dir_sep','')

    envp=cus.get('env_prefix','')

    fp=cus.get('full_path','')
    p1=os.path.dirname(fp)
    pi=os.path.dirname(p1)

    pb=pi+sdirs+'bin'
    pl=pi+sdirs+'lib'

    winh=host_d.get('windows_base','')

    cus['path_bin']=pb
    cus['path_lib']=pl

    ep=cus.get('env_prefix','')
    if pi!='' and ep!='':
       env[ep]=pi
       env[ep+'_BIN']=pb

    ################################################################
    pv='gcc-plugin-ici2'
    cus['ici_plugin_ver']=pv

    plug1=os.path.join(pl, pv+'-extract-program-structure.so')
    plug2=os.path.join(pl, pv+'-extract-program-static-features.so')
    fx1=os.path.join(pb,'featlstn.P')
    fx2=os.path.join(pb,'featlstn.P')

    if winh=='yes':
       r=ck.access({'action':'convert_to_cygwin_paths',
                    'module_uoa':'os',
                    'paths':{'pl':pl, 'plug1':plug1, 'plug2':plug2, 'fx1':fx1, 'fx2':fx2}})
       if r['return']>0: return r
       pp=r['paths']

       plug1=pp['plug1']
       plug2=pp['plug2']
       fx1=pp['fx1']
       fx2=pp['fx2']

       env['CCC_ICI_PASSES_RECORD_PLUGIN_CC']=pp['pl']+'/c'+pv+'-extract-program-structure.so'
       env['CCC_ICI_PASSES_RECORD_PLUGIN_FC']=pp['pl']+'/fortan'+pv+'-extract-program-structure.so'
       env['CCC_ICI_PASSES_RECORD_PLUGIN_CPP']=pp['pl']+'/cpp'+pv+'-extract-program-structure.so'

       env['CCC_ICI_FEATURES_ST_EXTRACT_PLUGIN_CC']=pp['pl']+'/c'+pv+'-extract-program-static-features.so'
       env['CCC_ICI_FEATURES_ST_EXTRACT_PLUGIN_FC']=pp['pl']+'/fortran'+pv+'-extract-program-static-features.so'
       env['CCC_ICI_FEATURES_ST_EXTRACT_PLUGIN_CPP']=pp['pl']+'/cpp'+pv+'-extract-program-static-features.so'

    env['ICI2_PLUGIN_VER']=pv
    env['ICI_PLUGIN_VER']=pv
    env['ICI_LIB']=pl
    env['CCC_ICI_USE']='ICI_USE'
    env['CCC_ICI_PLUGINS']='ICI_PLUGIN'
    env['CCC_ICI_PASSES_FN']='ici_passes_function'
    env['CCC_ICI_PASSES_EXT']='.txt'
    env['CCC_ICI_PASSES_RECORD_PLUGIN']=plug1
    env['CCC_ICI_FEATURES_ST_FN']='ici_features_function'
    env['CCC_ICI_FEATURES_ST_EXT']='.ft'
    env['CCC_ICI_FEATURES_ST_EXTRACT_PLUGIN']=plug2
    env['ICI_PROG_FEAT_PASS']='fre'
    env['ML_ST_FEAT_TOOL']=fx1
    env['ICI_PROG_FEAT_EXT_TOOL']=fx2

    return {'return':0, 'bat':s}
