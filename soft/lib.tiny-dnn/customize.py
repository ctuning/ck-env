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

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    win=hosd.get('windows_base','')

    ck=i['ck_kernel']

    fp=i['full_path']

    ver=''

    p0=os.path.basename(fp)
    p1=os.path.dirname(fp)
    p2=os.path.dirname(p1)

    px=os.path.join(p2,'docs','conf.py')
    print (px)
    if os.path.isfile(px):
        r=ck.load_text_file({'text_file':px, 'split_to_list':'yes'})
        if r['return']>0: return r

        lst=r['lst']

        for l in lst:
            j1=l.find('version =')
            if j1>=0:
                j2=l.find('\'', j1+1)
                if j2>0:
                    j3=l.find('\'',j2+1)
                    if j3>0:
                        ver=l[j2+1:j3]
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

    # Check platform
    hplat=hosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    sdirs=hosd.get('dir_sep','')

    env=i['env']

    ep=cus['env_prefix']

    p1=os.path.dirname(fp)
    p2=os.path.dirname(p1)
    pi=os.path.dirname(p2)

    env[ep]=pi

    cus['path_include']=p2
    env[ep+'_INCLUDE']=p2

    return {'return':0, 'bat':s}
