#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

##############################################################################
# internal: select extension
def get_ext(i):

    plat=i.get('processor','')

    ext=''
    if plat=='x86': 
         ext='x86'
    elif plat=='x64': 
         ext='amd64'
    elif plat=='arm': 
         ext='arm'
    else: 
       return {'return':1, 'error':'target platform ('+plat+') is not supported by this software'}

    return {'return':0, 'ext':ext}

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

    # Check platform
    plat=tosd.get('processor','')

    rx=get_ext({'processor':plat})
    if rx['return']>0: return rx
    ext=rx['ext']

    cmd=''
    if fp!='':
       cmd+=xnout+'call '+fp+' '+ext+'\n'
    cmd+=xnout+'cl '+cmdx+'\n'

    return {'return':0, 'cmd':cmd}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip()
        if q!='':
           j1=q.lower().find('compiler version ')
           if j1>0:
              q=q[j1+17:]
              j2=q.lower().find(' for')
              if j2>=0:
                 ver=q[:j2]
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

    hos=i['host_os_uid']
    tos=i['host_os_uid']
    tdid=i['target_device_id']

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    if 'android' in tosd.get('tags',[]):
       return {'return':1, 'error':'this software is not supporting Android platform'}

    # Check platform
    plat=tosd.get('processor','')

    # Check which processor
    rx=get_ext({'processor':plat})
    if rx['return']>0: return rx
    ext=rx['ext']

    env=i['env']

    ep=cus.get('env_prefix','')
    pi=''
    if fp!='' and ep!='':
       p1=os.path.dirname(fp)
       pi=os.path.dirname(p1)
       env[ep]=pi

    ############################################################
    s+='\n'
    s+='rem Setting environment\n'

    s+='call "'+fp+'" '+ext+'\n\n'

    env['VSINSTALLDIR']=pi

    # Attempt to detect path to compiler
    cmd=s+'where cl.exe'

    r=ck.access({'action':'shell',
                 'module_uoa':'os',
                 'host_os':hos,
                 'target_os':tos,
                 'device_id':tdid,
                 'cmd':cmd,
                 'split_to_list':'yes'})
    if r['return']>0: return r

    pcl=''
    for x in reversed(r['stdout_lst']):
        x=x.strip()
        if x!='':
           if os.path.isfile(x):
              pcl=x
           break

    if pcl!='':
       # Found compiler path (useful for CMAKE)
       env[ep+'_BIN']=os.path.dirname(pcl)

       ck.out('')
       ck.out('  * Found compiler in '+pcl)

    return {'return':0, 'bat':s}
