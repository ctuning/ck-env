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

def dirs(i):
    return {'return':0}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    if len(lst)>0:
        x=lst[0]
        j=x.find(' CE ')
        if j>0:
            j1=x.find(' Device',j+1)
            if j1>0:
                ver=x[j+3:j1].strip()

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

    env=i.get('env',{})
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})
    tags=i.get('tags',[])
    cus=i.get('customize',{})

    host_d=i.get('host_os_dict',{})
    target_d=i.get('target_os_dict',{})
    winh=host_d.get('windows_base','')
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus['env_prefix']
    fp=cus['full_path']
    pb=os.path.dirname(fp)

    pp=os.path.dirname(pb)
    pi=os.path.join(pp,'include')
    pl=os.path.join(pp,'lib')

    cus['path_bin']=pb
    cus['path_lib']=pl
    cus['path_include']=pi+'\\include'

    env[envp]=pp

    r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': host_d, 
      'dynamic_lib_path': pl})
    if r['return']>0: return r
    s += r['script']

    return {'return':0, 'bat':s, 'env':env, 'tags':tags}
