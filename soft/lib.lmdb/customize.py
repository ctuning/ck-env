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
    fp=cus.get('full_path','')

    p0=os.path.basename(fp)
    p1=os.path.dirname(fp)
    pi=os.path.dirname(p1)

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    # Check platform
    hplat=hosd.get('ck_name','')
    tplat=tosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    env=i['env']

    ep=cus['env_prefix']

    found=False
    while True:
       if os.path.isdir(os.path.join(pi,'lib')):
          found=True
          break
       pix=os.path.dirname(pi)
       if pix==pi:
          break
       pi=pix

    if not found:
       return {'return':1, 'error':'can\'t find root dir of this installation'}

    ############################################################
    # Setting environment depending on the platform
    cus['path_lib']=p1
    cus['path_include']=os.path.join(pi,'include')

    
    if tplat=='win':
       lbs='lmdb.lib'

       r=ck.access({'action':'convert_to_cygwin_path', 'module_uoa':'os', 'path':cus['path_lib']})
       if r['return']>0: return r
       cus['path_lib']=r['path']

       r=ck.access({'action':'convert_to_cygwin_path', 'module_uoa':'os', 'path':cus['path_include']})
       if r['return']>0: return r
       cus['path_include']=r['path']

    else:
       lbs='liblmdb.a'

    cus['static_lib']=lbs
    env[ep+'_STATIC_NAME']=lbs

    env[ep]=pi

    return {'return':0, 'bat':s}
