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
          ra=ck.inp({'text':'Enter compiler name prefix, if needed (such as aarch64-linux-android-): '})
          prefix=ra['string'].strip()
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
          ra=ck.inp({'text':'Enter full path to pre-built Android tools (such as ...prebuilt/linux-x86_64/bin) : '})
          extra_path=ra['string']
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
          ra=ck.inp({'text':'Enter full path to directory with Android NDK platforms : '})
          platform_path=ra['string']
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

    ############################################################
    libstdcpppathi_configured=cus.get('libstdcpppath_include_configured','')
    libstdcpppathi=cus.get('libstdcpppath_include','')
    if libstdcpppathi_configured!='yes' and iv=='yes':
       if libstdcpppathi!='':
          ck.out('Full path to include directory with libstdc++: '+libstdcpppathi)
       else:
          ra=ck.inp({'text':'* If needed, enter full path to include directory with libstdc++ (such as ...sources/cxx-stl/gnu-libstdc++/4.9/include: '})
          libstdcpppathi=ra['string']
          cus['libstdcpppath_include_configured']='yes'

    cus['libstdcpppath_include']=libstdcpppathi
    env['CK_ENV_LIB_STDCPP_INCLUDE']=libstdcpppathi
    cus['libstdcpppath_include_configured']='yes'

    libstdcpppath_configured=cus.get('libstdcpppath_configured','')
    libstdcpppath=cus.get('libstdcpppath','')
    if libstdcpppath_configured!='yes' and iv=='yes':
       if libstdcpppath!='':
          ck.out('Full path to include directory with libstdc++: '+libstdcpppath)
       else:
          ra=ck.inp({'text':'* If needed, enter full path to lib directory with libstdc++ (such as ...sources/cxx-stl/gnu-libstdc++/4.9/libs/armeabi-v7a: '})
          libstdcpppath=ra['string']
          cus['libstdcpppath_configured']='yes'

    if winh=='yes':
       sep='\\'
    else:
       sep='/'

    cus['libstdcpppath']=libstdcpppath
    if libstdcpppath!='':
       env['CK_ENV_LIB_STDCPP_STATIC']=libstdcpppath+sep+'libgnustl_static.a'
       env['CK_ENV_LIB_STDCPP_DYNAMIC']=libstdcpppath+sep+'libgnustl_shared.so'
       env['CK_ENV_LIB_STDCPP_INCLUDE_EXTRA']=libstdcpppath+sep+'include'
    else:
       env['CK_ENV_LIB_STDCPP_STATIC']=''
       env['CK_ENV_LIB_STDCPP_DYNAMIC']=''
       env['CK_ENV_LIB_STDCPP_INCLUDE_EXTRA']=''
    cus['libstdcpppath_configured']='yes'

    ############################################################
    ef_configured=cus.get('ef_configured','')
    ef=cus.get('ef','')
    if ef_configured!='yes' and iv=='yes':
       ra=ck.inp({'text':'Force extra flags, if needed (such as -fPIE -pie for aarch64): '})
       ef=ra['string']
       cus['ef']=ef
       cus['ef_configured']='yes'

    ##############
    if winh=='yes':
       psysroot=platform_path+'\\'+platform+'\\arch-'+arch
    else:
       psysroot=platform_path+'/'+platform+'/arch-'+arch
    sysroot='--sysroot "'+psysroot+'"'

    env['CK_SYS_ROOT']=psysroot

    x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
    if sysroot not in x:
       x=sysroot+' '+x

    if ef not in x:
       x+=' '+ef
    env['CK_COMPILER_FLAGS_OBLIGATORY']=x

#    x=env.get('CK_LD_FLAGS_EXTRA','')
#    if sysroot not in x:
#       x=sysroot+' '+x
#    env['CK_LD_FLAGS_EXTRA']=x

    return {'return':0, 'bat':s, 'env':env, 'tags':tags, 'cus':cus}
