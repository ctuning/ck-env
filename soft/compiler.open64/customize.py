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

    if pi=='':
       fp=cus.get('full_path','')
       p1=os.path.dirname(fp)
       pi=os.path.dirname(p1)

    ############################################################
    # Ask a few more questions
    prefix_configured=cus.get('tool_prefix_configured','')
    prefix=cus.get('tool_prefix','')
    if prefix_configured!='yes' and iv=='yes':
       if prefix!='':
          ck.out('Current compiler name prefix: '+prefix)
       else:
          ra=ck.inp({'text':'Compiler name prefix, if needed (such as "arm-none-linux-gnueabi-"): '})
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

    retarget=cus.get('retarget','')
    lfr=cus.get('linking_for_retargeting','')
    if retarget=='' and iv=='yes':
       ra=ck.inp({'text':'Using retargeting (for example, for ARM) (y/N)? '})
       x=ra['string'].strip().lower()
       if x!='' and x=='y' or x=='yes':
          retarget='yes'
          cus['retarget']='yes'
          if 'retargeted' not in tags: tags.append('retargeted')

          if lfr=='' and iv=='yes':
             y='-Wl,-dynamic-linker,/data/local/tmp/ld-linux.so.3 -Wl,--rpath -Wl,/data/local/tmp -lm -ldl'

             ra=ck.inp({'text':'LD extra flags for retargeting, if needed (or Enter for "'+y+'"): '})
             lfr=ra['string']

             if lfr=='': lfr=y

       else:
          cus['retarget']='no'

    if retarget=='yes' and lfr!='':
       cus['linking_for_retargeting']=lfr
       env['CK_LD_FLAGS_EXTRA']=lfr

    env['CK_COMPILER_TOOLCHAIN_NAME']='open64'

    add_m32=cus.get('add_m32','')
    if env.get('CK_COMPILER_ADD_M32','').lower()=='yes' or os.environ.get('CK_COMPILER_ADD_M32','').lower()=='yes':
       add_m32='yes'
       cus['add_m32']='yes'

#    if add_m32=='' and iv=='yes' and tbits=='32':
#       ra=ck.inp({'text':'Target OS is 32 bit. Add -m32 to compilation flags (y/N)? '})
#       x=ra['string'].strip().lower()
#       if x=='y' or x=='yes': 
#          add_m32='yes'
#          cus['add_m32']='yes'

    x=cus.get('add_extra_path','')
    if x!='':
       s+='\nset PATH='+pi+x+';%PATH%\n\n'

    return {'return':0, 'bat':s, 'env':env, 'tags':tags}
