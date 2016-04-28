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
# prepare env

def version_cmd(i):

    fp=i['full_path']

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']
    cmdx=i['cmd']

    o=i.get('out','')

    nout=hosd.get('no_output','')
    xnout=''
    if o!='con':
       xnout=nout

    eifsc=hosd.get('env_quotes_if_space_in_call','')

    if eifsc!='' and fp.find(' ')>=0 and not fp.startswith(eifsc):
       fp=eifsc+fp+eifsc

    cmd=''
    if fp!='':
       cmd =xnout+'call '+fp+'\n'
    cmd+=xnout+'amplxe-cl '+cmdx+'\n'

    return {'return':0, 'cmd':cmd}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip()
        if q!='':
           j=q.lower().find('vtune(tm) ')
           if j>=0:
              q=q[j+10:]
              j=q.find(' (')
              if j>=0:
                 ver=q[:j]
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
    if fp!='' and ep!='':
       pi=os.path.dirname(fp)
       env[ep]=pi

    ################################################################
    s+='\n'
    s+=host_d.get('rem','')+' Setting Intel compiler environment\n'

    x='bat'
    if winh!='yes': x='sh'

    s+=host_d.get('env_call','')+' "'+fp+'"\n\n'

    return {'return':0, 'bat':s}
