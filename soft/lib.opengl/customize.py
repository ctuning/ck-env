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
# get version from path

def version_cmd(i):

    ck=i['ck_kernel']

    fp=i['full_path']

    ver=''

    p0=os.path.basename(fp)
    p1=os.path.dirname(fp)

    lst=os.listdir(p1)
    for fn in lst:
        if fn.startswith(p0):
           x=fn[len(p0):]
           if x.startswith('.'):
              ver=x[1:]
              break

    return {'return':0, 'cmd':'', 'version':ver}

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

    # Get variables
    ck=i['ck_kernel']
    s=''

    iv=i.get('interactive','')

    cus=i.get('customize',{})
    fp=os.path.abspath(cus.get('full_path',''))

    p0=os.path.basename(fp)
    pl=os.path.dirname(fp)
    px=os.path.dirname(pl)

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    # Check platform
    hplat=hosd.get('ck_name','')

    ttags=tosd.get('tags',[])

    win=tosd.get('windows_base','')
    mingw=tosd.get('mingw','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    env=i['env']

    found=False
    pinc=pl
    while True:
       if os.path.isdir(os.path.join(pinc, 'include', 'GL')):
          found=True
          break
       pinc1=os.path.dirname(pinc)
       if pinc1==pinc:
          break
       pinc=pinc1

    if not found:
       return {'return':1, 'error':'can\'t find "include/GL" dir for this installation'}

    pinc=os.path.join(pinc,'include')

    ep=cus['env_prefix']
    env[ep]=px

    ############################################################
    cus['path_lib']=pl
    cus['path_include']=pinc

    r = ck.access({'action': 'lib_path_export_script', 
                   'module_uoa': 'os', 
                   'host_os_dict': hosd, 
                   'lib_path': cus.get('path_lib', '')})
    if r['return']>0: return r
    s += r['script']

    cus['dynamic_lib']=p0
    env[ep+'_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    if win!='yes':
       env[ep+'_LFLAG']='-lGL'

    return {'return':0, 'bat':s}
