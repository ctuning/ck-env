#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os

extra_dirs=['C:\\Qt', 'D:\\Qt']

##############################################################################
# customize directories to automatically find and register software

def dirs(i):

    hosd=i['host_os_dict']
    phosd=hosd.get('ck_name','')
    dirs=i.get('dirs', [])

    if phosd=='win':
        for d in extra_dirs:
            if os.path.isdir(d):
                dirs.append(d)

    return {'return':0, 'dirs':dirs}

##############################################################################
# limit directories 

def limit(i):

    dr=i.get('list',[])
    drx=[]

    for q in dr:
        if q.find('.libs')<0:
           drx.append(q)

    return {'return':0, 'list':drx}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    import re

    version_rgx = re.compile('Using Qt version ([\\d.]+) in');

    for q in lst:
        q = q.strip()
        match = version_rgx.search(q)
        if match:
          ver = match.group(1)
          break

    return {'return':0, 'version':ver}


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

    cus=i.get('customize',{})
    fp=cus.get('full_path','')

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    win=tosd.get('windows_base','')
    winh=hosd.get('windows_base','')

    # Check platform
    hplat=hosd.get('ck_name','')
    tplat=tosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    env=i['env']
    ep=cus['env_prefix']

    pinc=fp
    fpinc=''
    found=False
    while True:
       fpinc=os.path.join(pinc,'include')
       if os.path.isdir(fpinc):
          found=True
          break

       pincx=os.path.dirname(pinc)
       if pincx==pinc:
          break

       pinc=pincx

    if not found:
       return {'return':1, 'error':'can\'t find include directory for Qt'}

    pi=os.path.realpath(os.path.dirname(fpinc))

    pii=os.path.dirname(pi)

    lb=os.path.basename(fp)
    lbs=lb
    if lbs.endswith('.so'):
       lbs=lbs[:-3]+'.a'
    elif lbs.endswith('.lib'):
       lbs=lbs[:-4]+'.dll'

    pl=os.path.realpath(os.path.dirname(fp))
    cus['path_lib']=pl

    pl1=os.path.dirname(pl)
    pl2=os.path.dirname(pl1)

    cus['path_include']=pi

    cus['static_lib']=lb
    cus['dynamic_lib']=lbs

    r = ck.access({'action': 'lib_path_export_script', 
                   'module_uoa': 'os', 
                   'host_os_dict': hosd, 
                   'lib_path': cus.get('path_lib','')})
    if r['return']>0: return r
    s += r['script']

    env[ep]=pii

    pb=os.path.join(pii,'bin')
    if os.path.isdir(pb):
       env[ep+'_BIN']=pb
       cus['path_bin']=pb
       if tplat=='win':
          s+='\nset PATH='+pb+';%PATH%\n\n'

    env[ep+'_STATIC_NAME']=cus.get('static_lib','')
    env[ep+'_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    return {'return':0, 'bat':s}
