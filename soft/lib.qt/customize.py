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

qt_lib_path='' # will be filled as a side-effect of 'parse_version'. There should be a better way to do it...

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

    hosd=i.get('host_os_dict',{})
    tosd=i.get('target_os_dict',{})

    phosd=hosd.get('ck_name','')
    phosd2=hosd.get('ck_name2','')

    thosd=tosd.get('ck_name','')
    thosd2=tosd.get('ck_name2','')
    tbits=tosd.get('bits','')

    dr=i.get('list',[])
    drx=[]

    for q in dr:
        if q.find('.libs')>=0 or q.find('pkgs')>=0:
           continue
        
        if thosd2=='win' and (q.find('mingw')>0 or q.find('winrt')>0):
           continue

        if thosd2=='mingw' and (q.find('msvc')>0 or q.find('winrt')>0):
           continue

        if tbits=='64' and q.find('_32')>0:
           continue

        if tbits=='32' and q.find('_64')>0:
           continue

        drx.append(q)

    return {'return':0, 'list':drx}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver = ''
    global qt_lib_path

    import re

    version_rgx = re.compile('Using Qt version ([\\d.]+) in (.+)');

    for q in lst:
        q = q.strip()
        match = version_rgx.search(q)
        if match:
          ver = match.group(1)
          qt_lib_path = match.group(2)
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

    env[ep + '_QMAKE_EXE'] = fp

    global qt_lib_path
    env[ep + '_LIB'] = qt_lib_path

    bat = ''
    r = ck.access({'action': 'lib_path_export_script',
                   'module_uoa': 'os',
                   'host_os_dict': hosd,
                   'lib_path': qt_lib_path})
    if r['return']>0: return r
    bat += r['script']

    return {'return':0, 'bat': bat, 'env': env}
