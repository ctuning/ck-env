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

    # Ask a few more questions
    prefix=cus.get('tool_prefix','')
    if prefix=='' and iv=='yes':
       prefix=raw_input('Compiler name prefix, if needed (such as "arm-none-linux-gnueabi-"): ')

    retarget=cus.get('linking_for_retargeting','')
    if retarget=='' and iv=='yes':
       x=raw_input('Using retargeting (for example, for ARM) (y/N)? ')
       x=x.lower()
       if x!='' and x=='y' or x=='yes':
          y='-Wl,-dynamic-linker,/data/local/tmp/ld-linux.so.3 -Wl,--rpath -Wl,/data/local/tmp -lm -ldl'
          retarget=raw_input('LD extra flags for retargeting (or Enter for "'+y+'"): ')
          if retarget=='': retarget=y

    if retarget!='':
       env['CK_LD_FLAGS_EXTRA']=retarget
       if 'retargeted' not in tags: tags.append('retargeted')

    add_m32=cus.get('add_m32','')
    if add_m32=='' and iv=='yes':
       x=raw_input('Target OS is 32 bit. Add -m32 to compilation flags (y/N)? ')
       x=x.lower()
       if x=='y' or x=='yes': add_m32='yes'

    if prefix!='':
       env['CK_COMPILER_PREFIX']=prefix

    for k in env:
        v=env[k]

        v=v.replace('$#tool_prefix#$',prefix)

        if wb=='yes':
           if k=='CK_COMPILER_FLAGS_OBLIGATORY': 
              v=v+' -DWINDOWS'
              if tbits=='32': 
                 if add_m32=='yes': v+=' -m32'

           if k=='CK_CXX': v=v+' -fpermissive'   

        env[k]=v

    return {'return':0, 'bat':s, 'env':env, 'tags':tags, 'deps':deps}
