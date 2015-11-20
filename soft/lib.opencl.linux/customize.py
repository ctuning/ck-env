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
    win=target_d.get('windows_base','')
    winh=host_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    ################################################################
    cus['include_name']='CL/opencl.h'

    pl=os.path.join(pi,'lib')

    # On some Ubuntu there can be extra dir such as x86_64-linux-gnu
    # reported by Michael Kruse

    dir_extra_configured=cus.get('tool_dir_extra_configured','')
    dir_extra=cus.get('tool_dir_extra','')
    if dir_extra_configured!='yes':
       if dir_extra!='':
          ck.out('Current extra dir: '+dir_extra)
       else:
          dir_extra=raw_input('Enter extra directory if needed (such as x86_64-linux-gnu on Ubuntu) or Enter to skip it: ')
          cus['tool_dir_extra_configured']='yes'

    if dir_extra!='':
       pl=os.path.join(pl,dir_extra)

    cus['static_lib']='libOpenCL.so'
    cus['dynamic_lib']='libOpenCL.so'

    if not os.path.isfile(os.path.join(pl,cus['dynamic_lib'])):
       return {'return':1, 'error':cus['dynamic_lib']+' is not in lib directory - please install OpenCL driver or check paths'}

    env['CK_ENV_LIB_OPENCL_INCLUDE_NAME']=cus.get('include_name','')
    env['CK_ENV_LIB_OPENCL_STATIC_NAME']=cus.get('static_lib','')
    env['CK_ENV_LIB_OPENCL_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    return {'return':0, 'bat':s}
