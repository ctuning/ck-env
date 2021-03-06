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

    dr=i.get('list',[])
    drx=[]

    for q in dr:
        if q.find('.libs')<0:
           drx.append(q)

    return {'return':0, 'list':drx}

##############################################################################
# get version from path

def version_cmd(i):

    ck=i['ck_kernel']

    fp=i['full_path']
    fn=os.path.basename(fp)

    rfp=os.path.realpath(fp)
    rfn=os.path.basename(rfp)

    ver=''

    if rfn.startswith(fn):
       ver=rfn[len(fn)+1:]
       if ver!='':
          ver='api-'+ver

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

    import os

    # Get variables
    ck=i['ck_kernel']
    s=''

    iv=i.get('interactive','')

    cus=i.get('customize',{})
    fp=cus.get('full_path','')

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    # Check platform
    hplat=hosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    env=i['env']

    fi=cus.get('include_file','')

    pi=fp
    found=False
    while True:
       if os.path.isdir(os.path.join(pi,'lib')) or os.path.isdir(os.path.join(pi,'lib64')):
          found=True
          break
       pix=os.path.dirname(pi)
       if pix==pi:
          break
       pi=pix

    if not found:
       return {'return':1, 'error':'can\'t find root dir of this installation'}

    lb=os.path.basename(fp)
    lbs=lb
    if lbs.endswith('.so'):
       lbs=lbs[:-3]+'.a'

    pl=os.path.dirname(fp)
    cus['path_lib']=pl

    pl1=os.path.dirname(pl)
    pl2=os.path.dirname(pl1)

    pinc=''
    if os.path.isfile(os.path.join(pl1,'include',fi)):
       pi=pl1
       pinc=os.path.join(pl1,'include')
    elif os.path.isfile(os.path.join(pl2,'include',fi)):
       pi=pl2
       pinc=os.path.join(pl2,'include')
    elif os.path.isfile(os.path.join('/usr/include',fi)):
       pi='/usr'
       pinc='/usr/include'
    elif os.path.isfile(os.path.join(pl2,'include','arm-linux-gnueabihf',fi)):
       pi=pl2
       pinc=os.path.join(pl2,'include','arm-linux-gnueabihf')
    elif os.path.isfile(os.path.join('/usr/include/x86_64-linux-gnu',fi)):
       pi=pl2
       pinc='/usr/include/x86_64-linux-gnu'

    if pi=='':
       return {'return':1, 'error':'can\'t find include file'}

    cus['path_include']=pinc

    cus['include_name']=fi

    cus['static_lib']=lbs
    cus['dynamic_lib']=lb

    r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': hosd, 
      'lib_path': cus.get('path_lib','')})
    if r['return']>0: return r
    s += r['script']

    ep=cus.get('env_prefix','')
    if pi!='':
       env[ep]=pi

    env[ep+'_INCLUDE_NAME']=cus.get('include_name','')
    env[ep+'_STATIC_NAME']=cus.get('static_lib','')
    env[ep+'_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    return {'return':0, 'bat':s}
