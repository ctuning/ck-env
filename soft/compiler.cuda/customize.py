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

    target_d=i.get('target_os_dict',{})
    win=target_d.get('windows_base','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    ############################################################
    env['CUDA_PATH']=pi

    ############################################################
    if win=='yes':
       s+='\n'
       s+='rem Setting environment\n\n'

       s+='set PATH="'+pi+'\\bin"; "'+pi+'\\libnvvp"; "'+pi+'\\nnvm\\bin"; "'+pi+'\\open64\\bin"; %PATH%\n\n'

       env[envp+'_LIB']=pi+'\\lib'
       if tbits=='32':
          env[envp+'_LIB']+='\\Win32'

    return {'return':0, 'bat':s}
