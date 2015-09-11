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
       if remote=='yes':
          return {'return':1, 'error':'retargeting to ARM is supported in another soft description (*.arm)'}

       # Ask a few more questions
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
       if remote!='yes':
          if x.find('-DWINDOWS')<0: 
             x+=' -DWINDOWS' 
       if tbits=='32' and add_m32=='yes' and x.find('-m32')<0: 
          x+=' -m32' 

       y=cus.get('add_to_ck_compiler_flags_obligatory','')
       if y!='' and x.find(y)<0:
          x+=' '+y

       y='-target i686-pc-windows-msvc'
       if tbits=='64': y='-target x86_64-pc-windows-msvc'
       if x.find(y)<0:
          x+=' '+y

       env['CK_COMPILER_FLAGS_OBLIGATORY']=x

       if mingw=='yes': env['CK_MAKE']='mingw32-make'

       x=env.get('CK_CXX','')
       if x!='' and x.find('-fpermissive')<0:
          x+=' -fpermissive'
       env['CK_CXX']=x

       x=cus.get('add_extra_path','')
       if x!='':
          s+='\nset PATH='+pi+x+';%PATH%\n\n'

    return {'return':0, 'bat':s, 'env':env, 'tags':tags}
