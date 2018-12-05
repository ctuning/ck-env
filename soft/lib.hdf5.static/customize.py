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
        if q.find('.libs')<0 and q.find('anaconda')<0:
           drx.append(q)

    # Anaconda installation and libraries often conflict with existing OS installations

    return {'return':0, 'list':drx}

##############################################################################
# get version from path

def version_cmd(i):

    ck=i['ck_kernel']

    fp=i['full_path']

    ver=''

    r = ck.access({'action': 'search_version', 
                   'module_uoa': 'soft', 
                   'path': fp})
    if r['return']>0: return r
    ver=r.get('version','')

    if ver=='':
       if len(fp)>0:
          j=fp.rfind('.')
          if j>0:
             fps=fp[:j]+'.settings'
             if os.path.isfile(fps):
                # Load file and find setting
                r=ck.load_text_file({'text_file':fps, 'split_to_list':'yes'})
                if r['return']>0: return r

                for l in r['lst']:
                    l=l.strip()
                    if l.startswith('HDF5 Version:'):
                       ver=l[14:].strip()
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

    fi=cus.get('include_file','')

    pinc=fp
    fpinc=''
    found=False
    while True:
       fpinc=os.path.join(pinc,'include', fi)
       if os.path.isfile(fpinc):
          found=True
          break
       fpinc=os.path.join(pinc,'include','hdf5', 'serial', fi)
       if os.path.isfile(fpinc):
          found=True
          break
       pincx=os.path.dirname(pinc)
       if pincx==pinc:
          break
       pinc=pincx

    if not found:
       return {'return':1, 'error':'can\'t find include directory for HDF5'}

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
    cus['include_name']=fi

    cus['static_lib']=lb
    cus['dynamic_lib']=lbs

    r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': hosd, 
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

          env[ep+'_LFLAG']=os.path.join(pl,'hdf5.lib')
          env[ep+'_LFLAG_HL']=os.path.join(pl,'hdf5_hl.lib')

    env[ep+'_INCLUDE_NAME']=cus.get('include_name','')
    env[ep+'_STATIC_NAME']=cus.get('static_lib','')
    env[ep+'_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    return {'return':0, 'bat':s}
