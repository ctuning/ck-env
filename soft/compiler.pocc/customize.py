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
              deps         - resolved deps

              interactive  - if 'yes', ask questions

              (customize)  - external params for possible customization:

                             target_arm - if 'yes', target ARM
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat        - prepared string for bat file
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

    host_d=i.get('host_os_dict',{})
    target_d=i.get('target_os_dict',{})
    winh=host_d.get('windows_base','')
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    ############################################################
    # Ask a few more questions
    prefix=''

    for k in env:
        v=env[k]
        v=v.replace('$#tool_prefix#$',prefix)
        env[k]=v

    s+='\nexport PATH='+pi+'/bin:$PATH\n\n'

    return {'return':0, 'bat':s, 'env':env, 'tags':tags}
