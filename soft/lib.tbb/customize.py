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
              deps         - dependencies

              interactive  - if 'yes', ask questions

              (customize)  - external params for possible customization:

                             target_arm - if 'yes', target ARM
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
              env          - updated environment
              deps         - updated dependencies
              tags         - updated tags

              path         - install path
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
    mic=target_d.get('intel_mic','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    ################################################################
    ext='intel64'
    if remote=='yes':
       ext='android'
    elif mic=='yes':
       ext='mic'
    elif tbits=='32': 
       ext='ia32'

    s+='\n'

    # check visual studio extension
    if win=='yes':
       vsc=cus.get('visual_studio_compiler_configured','')
       vc=cus.get('visual_studio_compiler','')
       if vsc!='yes' or vc=='':
          vc=raw_input('Which Visual Studio Compiler configuration to use (Enter for vc12)? ')
          vc=vc.strip()
          if vc=='': vc='vc12'

          cus['visual_studio_compiler']=vc
          cus['visual_studio_compiler_configured']='yes'

       cus['path_bin']=pi+'\\bin\\'+ext+'\\'+vc
       cus['path_lib']=pi+'\\lib\\'+ext+'\\'+vc

       s+='rem Setting Intel TBB environment\n'
       s+='call "'+pi+'\\bin\\tbbvars.bat" '+ext+' '+vc+'\n'

    else:
       cus['path_bin']=pi+'/bin'
       cus['path_lib']=pi+'/lib/'+ext

       s+='# Setting Intel TBB environment\n'
       s+='. "'+pi+'\\bin\\tbbvars.sh" '+ext+' '+vc+'\n'

    return {'return':0, 'bat':s}
