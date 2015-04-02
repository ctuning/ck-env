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

    soft_name=i.get('soft_name','')

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

    ############################################################
    prefix_configured=cus.get('tool_prefix_configured','')
    prefix=cus.get('tool_prefix','')
    if prefix_configured!='yes' and iv=='yes':
       if prefix!='':
          ck.out('Current compiler name prefix: '+prefix)
       else:
          prefix=raw_input('Enter compiler name prefix, if needed (such as aarch64-linux-android-): ')
          cus['tool_prefix_configured']='yes'

    if prefix!='':
       env['CK_COMPILER_PREFIX']=prefix
       cus['tool_prefix']=prefix
       cus['tool_prefix_configured']='yes'

    for k in env:
        v=env[k]
        v=v.replace('$#tool_prefix#$',prefix)
        env[k]=v

    ############################################################
    extra_path_configured=cus.get('add_extra_path_configured','')
    extra_path=cus.get('add_extra_path','')
    if extra_path_configured!='yes' and iv=='yes':
       if extra_path!='':
          ck.out('Full path to pre-built Android tools: '+extra_path)
       else:
          extra_path=raw_input('Enter full path to pre-built Android tools (such as prebuilt/linux-x86_64/bin) : ')
          cus['extra_path_configured']='yes'

    if extra_path!='':
       cus['add_extra_path']=extra_path
       cus['add_extra_path_configured']='yes'

    if extra_path!='':
       if winh=='yes':
          s+='\nset PATH='+extra_path+';%PATH%\n\n'
       else:
          s+='\nexport PATH='+extra_path+':$PATH\n\n'

    ############################################################
    platform_path_configured=cus.get('platform_path_configured','')
    platform_path=cus.get('platform_path','')
    if platform_path_configured!='yes' and iv=='yes':
       if platform_path!='':
          ck.out('Full path to directory with Android NDK platforms: '+platform_path)
       else:
          platform_path=raw_input('Enter full path to directory with Android NDK platforms : ')
          cus['platform_path_configured']='yes'

    if platform_path=='':
       return {'return':1, 'error':'path to Android platforms is not defined'}

    cus['platform_path']=platform_path
    cus['platform_path_configured']='yes'

    ############################################################
    platform=target_d.get('android_ndk_platform','')
    if platform=='':
       return {'return':1, 'error':'platform is not defined in target OS'}

    ############################################################
    arch=target_d.get('android_ndk_arch','')
    if arch=='':
       return {'return':1, 'error':'platform architecture is not defined in target OS'}

    ##############
    if winh=='yes':
       sysroot='--sysroot "'+platform_path+'\\'+platform+'\\arch-'+arch+'"'
    else:
       sysroot='--sysroot "'+platform_path+'/'+platform+'/arch-'+arch+'"'

    x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
    if sysroot not in x:
       x=sysroot+' '+x
    env['CK_COMPILER_FLAGS_OBLIGATORY']=x

#    x=env.get('CK_LD_FLAGS_EXTRA','')
#    if sysroot not in x:
#       x=sysroot+' '+x
#    env['CK_LD_FLAGS_EXTRA']=x

    return {'return':0, 'bat':s, 'env':env, 'tags':tags, 'cus':cus}
