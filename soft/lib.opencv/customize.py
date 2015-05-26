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
    # check visual studio extension
    if win=='yes':
       ext='x64'
       if tbits=='32': ext='ia32'

       # Check where bin/libs are installed
       pc=cus.get('path_extension_configured','')
       pp=cus.get('path_extension','')

       if pc!='yes' and pp=='':
          pp=raw_input('Enter installation path extension related to compiler (Enter for vc12): ')
          pp=pp.strip()
          if pp=='': pp='vc12'

          cus['path_extension']=pp
          cus['path_extension_configured']='yes'

       cus['path_bin']=pi+ext+'\\'+pp+'\\bin'
       cus['path_lib']=pi+ext+'\\'+pp+'\\lib'

       # Check libs version extensions
       lec=cus.get('lib_extension_configured','')
       le=cus.get('lib_extension','')

       if lec!='yes' and le=='':
          le=raw_input('Enter lib extension (for example, 2411d for 2.4.11d): ')
          le=le.strip()

          cus['lib_extension']=le
          cus['lib_extension_configured']='yes'

       cus['path_bin']=pi+'\\'+ext+'\\'+pp+'\\bin'
       cus['path_lib']=pi+'\\'+ext+'\\'+pp+'\\lib'

       cus['path_static_lib']=pi+'\\'+ext+'\\'+pp+'\\lib'
       cus['path_dynamic_lib']=pi+'\\'+ext+'\\'+pp+'\\bin'

       cus['static_lib']='opencv_core'+le+'.lib'
       cus['dynamic_lib']='opencv_core'+le+'.dll'

       cus['extra_static_libs']={'opencv_imgproc':'opencv_imgproc'+le+'.lib',
                                 'opencv_ocl':'opencv_ocl'+le+'.lib',
                                 'opencv_highgui':'opencv_highgui'+le+'.lib'}
 
       cus['extra_dynamic_libs']={'opencv_imgproc':'opencv_imgproc'+le+'.dll',
                                  'opencv_ocl':'opencv_ocl'+le+'.dll',
                                  'opencv_highgui':'opencv_highgui'+le+'.dll'}

       env['CK_ENV_LIB_OPENCV_STATIC_LIB_PATH']=cus['path_static_lib']
       env['CK_ENV_LIB_OPENCV_DYNAMIC_LIB_PATH']=cus['path_dynamic_lib']

    else:
       cus['path_bin']=pi+'/bin'
       cus['path_lib']=pi+'/lib'

    return {'return':0, 'bat':s}
