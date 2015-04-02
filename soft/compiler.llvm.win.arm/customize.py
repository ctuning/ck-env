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
    if winh=='yes':
       if remote!='yes':
          return {'return':1, 'error':'this soft customization supported only (remote) ARM platforms'}

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

       # Ask a few more questions
       target_configured=cus.get('target_configured','')
       target=cus.get('target','')
       if target_configured!='yes' and iv=='yes':
          if target!='':
             ck.out('Current target: '+target)
          else:
             target=raw_input('Enter compiler target from GCC (arm-linux-androideabi, arm-none-linux-gnueabi, etc): ')
             cus['target_configured']='yes'

       if target=='':
          target='arm-none-linux-gnueabi'

       env['CK_LLVM_TARGET']=target
       cus['target']=target

       x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
       y='-target '+target+' -gcc-toolchain %CK_ENV_COMPILER_GCC% --sysroot=%CK_SYS_ROOT%'
       x=x.replace('$#flags_for_arm_target#$',y)

       env['CK_COMPILER_FLAGS_OBLIGATORY']=x

       x=env.get('CK_CXX','')
       if x!='' and x.find('-fpermissive')<0:
          x+=' -fpermissive'
       env['CK_CXX']=x

       x=cus.get('add_extra_path','')
       if x!='':
          s+='\nset PATH='+pi+x+';%PATH%\n\n'

    return {'return':0, 'bat':s, 'env':env, 'tags':tags}
