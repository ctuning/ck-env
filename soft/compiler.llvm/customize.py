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

import sys
if sys.version_info[0]>2:
   def raw_input(i):
       return input(i)

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
    if winh=='yes':
       return {'return':1, 'error':'this soft customization is for non-Windows target only'}

    # Ask a few more questions
    # (tool prefix)
    prefix_configured=cus.get('tool_prefix_configured','')
    prefix=cus.get('tool_prefix','')

    if prefix!='':
       env['CK_COMPILER_PREFIX']=prefix
       cus['tool_prefix']=prefix
       cus['tool_prefix_configured']='yes'

    for k in env:
        v=env[k]
        v=v.replace('$#tool_prefix#$',prefix)
        env[k]=v

    # (tool postfix such as -3.6)
    postfix_configured=cus.get('tool_postfix_configured','')
    postfix=cus.get('tool_postfix','')

    if postfix=='':
       print ('')
       postfix=raw_input('Input clang postfix if needed (for example, -3.6 for clang-3.6) or Enter to skip: ')
       postfix=postfix.strip()

    if postfix!='':
       env['CK_COMPILER_POSTFIX']=postfix
       cus['tool_postfix']=postfix
       cus['tool_postfix_configured']='yes'

    for k in env:
        v=env[k]
        v=v.replace('$#tool_postfix#$',postfix)
        env[k]=v

    retarget=cus.get('retarget','')
    lfr=cus.get('linking_for_retargeting','')

    if retarget=='yes' and lfr!='':
       cus['linking_for_retargeting']=lfr
       env['CK_LD_FLAGS_EXTRA']=lfr

    add_m32=cus.get('add_m32','')
    if add_m32=='' and iv=='yes' and tbits=='32':
       x=raw_input('Target OS is 32 bit. Add -m32 to compilation flags (y/N)? ')
       x=x.lower()
       if x=='y' or x=='yes': 
          add_m32='yes'
          cus['add_m32']='yes'

    x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
    if tbits=='32' and add_m32=='yes' and x.find('-m32')<0: 
       x+=' -m32' 

    y=cus.get('add_to_ck_compiler_flags_obligatory','')
    if y!='' and x.find(y)<0:
       x+=' '+y
    env['CK_COMPILER_FLAGS_OBLIGATORY']=x

    x=cus.get('add_extra_path','')
    if x!='':
       s+='\nset PATH='+pi+x+';%PATH%\n\n'

    return {'return':0, 'bat':s, 'env':env, 'tags':tags}
