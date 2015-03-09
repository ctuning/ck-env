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

    target_d=i.get('target_os_dict',{})
    win=target_d.get('windows_base','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    ############################################################
    if win=='yes':
       if mingw!='yes':
          return {'return':1, 'error':'target OS should be mingw-32 or mingw-64'}

       # Ask a few more questions
       prefix_configured=cus.get('tool_prefix_configured','')
       prefix=cus.get('tool_prefix','')
       if prefix_configured!='yes' and iv=='yes':
          if prefix!='':
             ck.out('Current compiler name prefix: '+prefix)
          else:
             prefix=raw_input('Compiler name prefix, if needed (such as "arm-none-linux-gnueabi-"): ')
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
       if retarget=='' and iv=='yes':
          x=raw_input('Using retargeting (for example, for ARM) (y/N)? ')
          x=x.lower()
          if x!='' and x=='y' or x=='yes':
             cus['retarget']='yes'
             if 'retargeted' not in tags: tags.append('retargeted')

             lfr=cus.get('linking_for_retargeting','')
             if lfr=='' and iv=='yes':
                y='-Wl,-dynamic-linker,/data/local/tmp/ld-linux.so.3 -Wl,--rpath -Wl,/data/local/tmp -lm -ldl'
                lfr=raw_input('LD extra flags for retargeting (or Enter for "'+y+'"): ')
                if lfr=='': lfr=y

                cus['linking_for_retargeting']=lfr
                env['CK_LD_FLAGS_EXTRA']=lfr
          else:
             cus['retarget']='no'

       add_m32=cus.get('add_m32','')
       if add_m32=='' and iv=='yes' and tbits=='32':
          x=raw_input('Target OS is 32 bit. Add -m32 to compilation flags (y/N)? ')
          x=x.lower()
          if x=='y' or x=='yes': 
             add_m32='yes'
             cus['add_m32']='yes'

       x=env.get('CK_COMPILER_FLAGS_OBLIGATORY','')
       if x.find('-DWINDOWS')<0: 
          x+=' -DWINDOWS' 
       if tbits=='32' and add_m32=='yes' and x.find('-m32')<0: 
          x+=' -m32' 
       env['CK_COMPILER_FLAGS_OBLIGATORY']=x

       if mingw=='yes': env['CK_MAKE']='mingw32-make'

       x=env.get('CK_CXX','')
       if x!='' and x.find('-fpermissive')<0:
          x+=' -fpermissive'
       env['CK_CXX']=x

    return {'return':0, 'bat':s, 'env':env, 'tags':tags}
