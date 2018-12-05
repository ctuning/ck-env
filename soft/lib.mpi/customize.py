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

    r = ck.access({'action': 'search_version', 
                   'module_uoa': 'soft', 
                   'path': fp})
    if r['return']>0: return r
    ver=r.get('version','')

    if ver=='':
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

    ep=cus['env_prefix']

    # Bin and root dir
    fp=os.path.realpath(fp)

    p1=os.path.dirname(fp)
    p2=os.path.dirname(p1)

    pb=os.path.join(p2, 'bin')
    if not os.path.isdir(pb):
       pbx=os.path.dirname(p2)
       pb=os.path.join(pbx,'bin')
       if not os.path.isdir(pb):
          return {'return':1, 'error':'can\'t find bin directory'}

    env[ep]=p2

    # Include dir
    pi=os.path.join(p2,'include')
    if not os.path.isdir(pi):
       return {'return':1, 'error':'can\'t find include directory'}

    # Lib dir
    pl=os.path.join(p2,'lib')
    if not os.path.isdir(pl):
       return {'return':1, 'error':'can\'t find lib directory'}

    cus['path_include']=pi
    cus['path_lib']=pl
    cus['path_bin']=pb

    # Check different compilers
    for q in [{'file':'mpicc', 'var':'_CC'},
              {'file':'mpicxx', 'var':'_CXX'},
              {'file':'mpifort', 'var':'_FC'},
              {'file':'mpirun', 'var':'_RUN'}]:
        bfile=q['file']
        if win=='yes': bfile+='.exe'
        xbfile=os.path.join(pb, bfile)
        if os.path.isfile(xbfile):
           env['CK_ENV_LIB_MPI'+q['var']] = bfile
           env['CK_ENV_LIB_MPI'+q['var']+'_FULL'] = xbfile

    # Prepare library paths
    r = ck.access({'action': 'lib_path_export_script', 
                   'module_uoa': 'os', 
                   'host_os_dict': hosd, 
                   'lib_path': cus.get('path_lib','')})
    if r['return']>0: return r
    s += r['script']

    return {'return':0, 'bat':s}
