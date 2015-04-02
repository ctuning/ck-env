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

    if remote=='yes': # Libraries are on remote device, use stubs
      cus['static_lib']='libOpenCL.so'
      cus['dynamic_lib']='libOpenCL.so'
    else:
      cus['static_lib']='libmali.so'
      cus['dynamic_lib']='libmali.so'

      if not os.path.isfile(os.path.join(pl,cus['dynamic_lib'])):
         return {'return':1, 'error':'libmali.so is not in lib directory - please copy driver libs there'}

    env['CK_ENV_LIB_OPENCL_INCLUDE_NAME']=cus.get('include_name','')
    env['CK_ENV_LIB_OPENCL_STATIC_NAME']=cus.get('static_lib','')
    env['CK_ENV_LIB_OPENCL_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    if remote=='yes':
       print ("")
       print ("Trying to compile OpenCL stubs lib ...")

       make=deps['compiler'].get('dict',{}).get('env',{}).get('CK_MAKE','')
       if make=='': make='make'

       if winh=='yes':
          x='CC="%CK_CXX%"'
       else:
          x='CC="$CK_CXX"'

       cmd=deps['compiler']['bat'].strip()+' '+host_d['env_separator']+' '+make+' '+x

       print ("")
       print (cmd)

       os.chdir(pl)
       rx=os.system(cmd)

    return {'return':0, 'bat':s}
