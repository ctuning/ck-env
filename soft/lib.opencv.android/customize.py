#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os

##############################################################################
# limit directories 

def limit(i):

    ck=i['ck_kernel']

    hosd=i.get('host_os_dict',{})
    tosd=i.get('target_os_dict',{})

    dr=i.get('list',[])
    drx=[]

    abi=tosd.get('abi','')
    if abi!='':
       for q in dr:
           if abi in q:
              drx.append(q)

    return {'return':0, 'list':drx}

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    import os

    # Get variables
    ck=i['ck_kernel']
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

    fp=cus.get('full_path','')
    pl=os.path.dirname(fp)
    p1=os.path.dirname(pl)
    p2=os.path.dirname(p1)
    pinc=os.path.join(p2,'jni','include')

    abi=target_d.get('abi','')
    if abi=='':
       abi='armeabi'

    cus['path_lib']=pl

    plx=os.path.join(p1,'3rdparty','libs',abi)

    cus['path_include']=pinc

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

    return {'return':0, 'bat':s}
