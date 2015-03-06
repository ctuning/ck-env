#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK Copyright.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://cTuning.org/lab/people/gfursin
#

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg          - dict of the soft entry
              tags         - list of tags
              env          - environment

              interactive  - if 'yes', ask questions

              (customize)  - external params for possible customization:

                             tool_prefix             - prefixing all tool names (XYZ-gcc)
                             linking_for_retargeting - if !='', add to env[CK_LD_FLAGS_EXTRA]
                             add_m32                 - if 'yes' and target OS is 32 bit, add -m32
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat        - prepared string for bat file
              env          - updated environment
              tags         - updated tags
            }

    """

    import os

    s=''

    iv=i.get('interactive','')
    if iv=='yes': print ('')

    deps=i.get('deps',{})
    env=i.get('env',{})
    cfg=i.get('cfg',{})
    cus=i.get('customize',{})
    tags=i.get('tags',[])

    tbits=i.get('target_os_bits','')

    target_d=i.get('target_os_dict',{})
    wb=target_d.get('windows_base','')

    envp=cfg.get('env_prefix','')


    return {'return':0, 'bat':s, 'env':env, 'tags':tags, 'deps':deps}
