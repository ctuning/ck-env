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

    host_d=i.get('host_os_dict',{})
    target_d=i.get('target_os_dict',{})
    winh=host_d.get('windows_base','')
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    fp=cus.get('full_path','')

    # Check path
    ep=cus.get('env_prefix','')
    if fp!='':
       p1=os.path.dirname(fp)
       pi=os.path.dirname(p1)

       if p1!='/usr/bin':
          cus['path_bin']=p1

       if ep!='':
          env[ep]=pi
          if p1!='/usr/bin': 
             env[ep+'_BIN']=p1

    ############################################################
    # Ask a few more questions
    prefix_configured=cus.get('tool_prefix_configured','')
    prefix=cus.get('tool_prefix','')

    env['CK_COMPILER_PREFIX']=prefix
    cus['tool_prefix']=prefix
    cus['tool_prefix_configured']='yes'

    for k in env:
        v=env[k]
        v=v.replace('$#tool_prefix#$',prefix)
        env[k]=v

    # (tool postfix such as -4.6)
    postfix_configured=cus.get('tool_postfix_configured','')
    postfix=cus.get('tool_postfix','')

    env['CK_COMPILER_POSTFIX']=postfix
    cus['tool_postfix']=postfix
    cus['tool_postfix_configured']='yes'

    for k in env:
        v=env[k]
        v=v.replace('$#tool_postfix#$',postfix)
        env[k]=v

    cus['retarget']='no'

    env['CK_COMPILER_TOOLCHAIN_NAME']='gcc'

    add_m32=cus.get('add_m32','')
    if env.get('CK_COMPILER_ADD_M32','').lower()=='yes' or os.environ.get('CK_COMPILER_ADD_M32','').lower()=='yes':
       add_m32='yes'
       cus['add_m32']='yes'

#    if add_m32=='' and iv=='yes' and tbits=='32':
#       ra=ck.inp({'text':'Target OS is 32 bit. Add -m32 to compilation flags (y/N)? '})
#       x=ra['string'].strip().lower()
#       x=x.lower()
#       if x=='y' or x=='yes': 
#          add_m32='yes'
#          cus['add_m32']='yes'

    if winh=='yes':
       x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
       if remote!='yes':
          if x.find('-DWINDOWS')<0: 
             x+=' -DWINDOWS' 
       if tbits=='32' and add_m32=='yes' and x.find('-m32')<0: 
          x+=' -m32' 
       env['CK_COMPILER_FLAGS_OBLIGATORY']=x

       if mingw=='yes': env['CK_MAKE']='mingw32-make'
       elif remote=='yes': env['CK_MAKE']='cs-make'

       x=env.get('CK_CXX','')
       if x!='' and x.find('-fpermissive')<0:
          x+=' -fpermissive'
       env['CK_CXX']=x

    x=cus.get('bugfix1','')
    if x=='yes' and winh!='yes':
       s+='\nexport LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LIBRARY_PATH\n'

    x=cus.get('add_extra_path','')
    if x!='' and winh=='yes':
       s+='\nset PATH='+pi+x+';%PATH%\n\n'

    # Add SRC env for plugins
    if winh=='yes':
       pii=os.path.dirname(pi)
       pii1=os.path.dirname(pii)
#       s+='\nset PATH='+pii1+'\\etc\\milepost-gcc-4.4.4-bin\\bin;'+pii1+'\\bin;'+pii1+'\\msys\\1.0\\bin;%PATH%\n\n'
#       We should not add MILEPOST GCC to the path since it may interfere with the main compiler

       s+='\nset PATH=%PATH%;'+pii1+'\\bin;'+pii1+'\\msys\\1.0\\bin\n\n'

       r=ck.access({'action':'convert_to_cygwin_paths',
                    'module_uoa':'os',
                    'paths':{'pii':pii, 'pi':pi}})
       if r['return']>0: return r
       pp=r['paths']

       s+='\nset CK_ENV_COMPILER_GCC_SRC='+pp['pii']+'/milepost-gcc-4.4.4\n\n'

       s+='\nset CK_ENV_COMPILER_GCC_LIB_GCC_PLUGIN='+pp['pi']+'/lib/libcc1.a\n'
       s+='\nset CK_ENV_COMPILER_GCC_LIB_GCC_PLUGIN_CC='+pp['pi']+'/lib/libcc1.a\n'
       s+='\nset CK_ENV_COMPILER_GCC_LIB_GCC_PLUGIN_FC='+pp['pi']+'/lib/libf951.a\n'
       s+='\nset CK_ENV_COMPILER_GCC_LIB_GCC_PLUGIN_CPP='+pp['pi']+'/lib/libcc1plus.a\n'

    else:
       s+='\nexport CK_ENV_COMPILER_GCC_SRC='+pi+'/milepost-gcc-4.4.4\n\n'

    # Otherwise may be problems on Windows during cross-compiling
    env['CK_OPT_UNWIND']=' '
    env['CK_FLAGS_DYNAMIC_BIN']=' '

    return {'return':0, 'bat':s, 'install_env':env, 'tags':tags}
