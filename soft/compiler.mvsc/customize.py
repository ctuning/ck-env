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

                             target_arm - if 'yes', target ARM
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat        - prepared string for bat file
              env          - updated environment
              tags         - updated tags

              path         - install path
            }

    """

    import os

    s=''

    iv=i.get('interactive','')
    if iv=='yes': print ('')

    env=i.get('env',{})
    cfg=i.get('cfg',{})
    cus=i.get('customize',{})
    tags=i.get('tags',[])

    tbits=i.get('target_os_bits','')

    target_d=i.get('target_os_dict',{})
    wb=target_d.get('windows_base','')

    envp=cfg.get('env_prefix','')

    pi=i.get('path','')

    s+='\n'
    s+='REM Setting environment\n'

    yy='call "'+pi+'\\vcvarsall.bat" '

    # Check which processor
    arm=cus.get('target_arm','')
    if target_d.get('remote','')=='yes' and arm=='':
       arm='yes'
       if iv=='yes':
          ck.out('You selected remote platform as a target.')

          x=raw_input('Do you target ARM processors (Y/n): ')
          if x!='' and x!='Y' and x!='yes': 
             arm='no'

    if arm=='yes':
       yy+=' x86_arm'
    else:
       if tbits=='32': yy+=' x86'
       else: yy+=' amd64'

    s+=yy+'\n\n'

    return {'return':0, 'bat':s, 'env':env, 'tags':tags}
