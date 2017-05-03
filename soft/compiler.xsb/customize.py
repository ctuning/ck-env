#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip()
        if q!='' and q.startswith('Python ') and len(q)>6:
           ver=q[7:]

           j=ver.find(' ::')
           if j>0:
              ver=ver[:j]   
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

    env=i.get('env',{})
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})
    tags=i.get('tags',[])
    cus=i.get('customize',{})

    host_d=i.get('host_os_dict',{})
    target_d=i.get('target_os_dict',{})
    winh=host_d.get('windows_base','')
    win=target_d.get('windows_base','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    fp=cus.get('full_path','')

    ep=cus.get('env_prefix','')
    p1=os.path.dirname(fp)
    pi=os.path.dirname(p1)

    env[ep]=pi
    env[ep+'_BIN']=p1

    ################################################################
    s+='\n'


    # check target
    p=os.path.join(pi,'config')
    ld0=''
    if os.path.isdir(p):
       ld=os.listdir(p)

       if len(ld)>0:
          ld0=ld[0]

    if winh=='yes':
       r=ck.access({'action':'convert_to_cygwin_paths',
                    'module_uoa':'os',
                    'paths':{'pi':pi, 'bin':p1, 'ld0':ld0}})
       if r['return']>0: return r
       pp=r['paths']

       env[ep]=pp['pi']
       env[ep+'_BIN']=pp['bin']

       s+='set XSB_DIR='+pp['pi']+'\n\n'
       s+='set XSB_DIR_ADD='+pp['ld0']+'\n\n'
    else:
       s+='export XSB_DIR='+pi+'\n\n'
       s+='export XSB_DIR_ADD='+ld0+'\n\n'

    return {'return':0, 'bat':s}
