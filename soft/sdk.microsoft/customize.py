#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

##############################################################################
# customize directories to automatically find and register software

import os

def dirs(i):
    return {'return':0}

##############################################################################
# customize directories to automatically find and register software

def limit(i):
    xlst=i['list']
    lst=[]

    for p in xlst:
        pp=os.path.join(p,'Windows')
        if os.path.isdir(pp):
           xx=os.listdir(pp)
           for fx in xx:
               px=os.path.join(pp,fx)
               if os.path.isdir(px) and fx.lower().startswith('v'):
                  lst.append(px)

    return {'return':0, 'list':lst}

##############################################################################
# get version from path

def version_cmd(i):

    fp=i['full_path']

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']
    cmdx=i['cmd']

    fp1=os.path.basename(os.path.normpath(fp))
    
    ver=''
    if len(fp1)>0:
       ver=fp1[1:]

    cmd=''

    return {'return':0, 'cmd':cmd, 'version':ver}

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
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')
    fp=cus.get('full_path','')

    ############################################################
    s+='\n'
    s+='rem Setting environment\n\n'

    env['CK_WINDOWS_SDK_PATH']=fp

    px='bin'
    if tbits=='64': px+='\\x64'
    p1=os.path.join(fp,px)
    if os.path.isdir(p1):
       s+='set PATH='+p1+';%PATH%\n'

    px='lib'
    if tbits=='64': px+='\\x64'
    p2=os.path.join(fp,px)
    if os.path.isdir(p2):
       s+='set LIB='+p2+';%LIB%\n'

    return {'return':0, 'bat':s}
