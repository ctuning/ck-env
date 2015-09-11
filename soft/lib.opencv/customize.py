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

    hosd=i.get('host_os_dict',{})

    ellp=hosd.get('env_ld_library_path','')
    if ellp=='': ellp='LD_LIBRARY_PATH'
    elp=hosd.get('env_library_path','')
    if elp=='': elp='LIBRARY_PATH'

    ################################################################
    if remote=='yes':
       cus['path_bin']=pi+'\\OpenCV-android-sdk\\sdk\\native\\bin'
       cus['path_lib']=pi+'\\OpenCV-android-sdk\\sdk\\native\\libs\\armeabi'

       cus['path_include']=pi+'\\opencv-2.4.11\\include'
       cus['path_includes']=[pi+'\\opencv-2.4.11\\3rdparty\\include\\opencl\\1.2']

       cus['path_static_lib']=cus['path_lib']

       cus['static_lib']='libopencv_core.a'

       cus['extra_static_libs']={'opencv_imgproc':'libopencv_imgproc.a',
                                  'opencv_ocl':'libopencv_ocl.a',
                                  'opencv_highgui':'libopencv_highgui.a'}

       env['CK_ENV_LIB_OPENCV_STATIC_LIB_PATH']=cus['path_static_lib']

       if win=='yes':
          s+='\nset '+ellp+'=%CK_ENV_LIB_OPENCV_LIB%;%'+ellp+'%\n'
       else:
          s+='\nexport '+ellp+'=$CK_ENV_LIB_OPENCV_LIB:$'+ellp+'\n'

    elif win=='yes':
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

       cus['path_include']=pi+'/include'

       cus['path_static_lib']=cus['path_lib']
       cus['path_dynamic_lib']=cus['path_lib']

       cus['dynamic_lib']='libopencv_core.so'

       cus['extra_dynamic_libs']={'opencv_imgproc':'libopencv_imgproc.so',
                                  'opencv_ocl':'libopencv_ocl.so',
                                  'opencv_highgui':'libopencv_highgui.so'}

       env['CK_ENV_LIB_OPENCV_STATIC_LIB_PATH']=cus['path_static_lib']
       env['CK_ENV_LIB_OPENCV_DYNAMIC_LIB_PATH']=cus['path_dynamic_lib']

       s+='\nexport '+ellp+'=$CK_ENV_LIB_OPENCV_LIB:$'+ellp+'\n'

    return {'return':0, 'bat':s}
