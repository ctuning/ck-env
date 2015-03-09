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

    host_d=i.get('host_os_dict',{})
    target_d=i.get('target_os_dict',{})
    winh=host_d.get('windows_base','')
    win=target_d.get('windows_base','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    ################################################################
    # Check which version of visual studio is used
    vs=''

    vsx=deps['compiler_mcl']
    ver=vsx.get('ver','')

    if ver.startswith('15.'): vs='vs2008shell'
    elif ver.startswith('18.'): vs='vs2013'
    else:
       if iv=='yes':
          vs=raw_input('Enter Visual Studio dependency (vs2008shell or vs2013):')
       else:
          return {'return':1, 'error':'Visual Studio version is not recognized - should be either 15.x or 18.x'}

    s+='\n'
    s+='rem Setting Intel compiler environment\n'

    yy='call "'+pi+'\\bin\\compilervars.bat" '

    if tbits=='32': yy+=' ia32'
    else: yy+=' intel64'

    s+=yy+' '+vs+'\n\n'

    return {'return':0, 'bat':s}
