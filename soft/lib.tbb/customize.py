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

       cus['static_lib']='tbb.lib'
       cus['extra_static_libs']={'libtbbmalloc':'tbbmalloc.lib',
                                 'libtbbproxy':'tbbproxy.lib'}

       cus['dynamic_lib']='libtbb.dll'
       cus['extra_dynamic_libs']={'libtbbmalloc':'tbb.dll',
                                  'libtbbproxy':'tbbproxy.dll'}

       s+='rem Setting Intel TBB environment\n'
       s+='call "'+pi+'\\bin\\tbbvars.bat" '+ext+' '+vc+'\n'

    else:
       if cus.get('from_sources','')=='yes':
          pix=pi+'/build/install_release'
          cus['path_lib']=pix
       else:
          cus['path_bin']=pi+'/bin'

          ext1=''
          if ext=='intel64' or ext=='ia32':
             # check extra params
             ext1=cus.get('extra_compiler','')
             ext1c=cus.get('extra_compiler_configured','')
             if ext1c!='yes' or ext1=='':
                ext1=raw_input('Which compiler configuration to use (Enter for gcc4.4)? ')
                ext1=ext1.strip()

                if ext1=='': ext1='gcc4.4'

                cus['extra_compiler']=ext1
                cus['extra_compiler_configured']='yes'

          pix=pi+'/lib/'+ext
          if ext1!='': pix+='/'+ext1
          cus['path_lib']=pix

       cus['path_dynamic_lib']=pix
       cus['dynamic_lib']='libtbb.so'
       cus['extra_dynamic_libs']={'libtbbmalloc':'libtbbmalloc.so'}

       s+='# Setting Intel TBB environment\n'
       s+='. "'+pix+'/tbbvars.sh"\n'

    return {'return':0, 'bat':s}
