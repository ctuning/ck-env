#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

extra_dirs=['C:\\Program Files (x86)\\Microsoft Visual Studio\\2017',
            'D:\\Program Files (x86)\\Microsoft Visual Studio\\2017']

import os

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
    dirs=i.get('dirs', [])
    for d in extra_dirs:
        if os.path.isdir(d):
            dirs.append(d)
    return {'return':0, 'dirs':dirs}

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
           j1=q.lower().find(' version')
           if j1>0:
              q=q[j1+9:]
              j2=q.lower().find(' ')
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

    ver=i.get('version','')
    sver=i.get('version_split',[])

    # Check platform
    plat=tosd.get('processor','')
    tbits=tosd.get('bits','')

    # Check which processor
    rx=get_ext({'processor':plat})
    if rx['return']>0: return rx
    ext=rx['ext']

    env=i['env']

    ep=cus['env_prefix']
    pi=''
    if fp!='' and ep!='':
       p1=os.path.dirname(fp)
       pi=os.path.dirname(p1)
       env[ep]=pi

    # Prepare cmake generator
    cgen=''
    if len(sver)>0:
       if sver[0]==19 and len(sver)>0 and sver[1]>0:
          cgen='Visual Studio 15 2017'
       elif sver[0]==19:
          cgen='Visual Studio 14 2015'
       elif sver[0]==18:
          cgen='Visual Studio 12 2013'
       elif sver[0]==17:
          cgen='Visual Studio 11 2012'
       elif sver[0]==16:
          cgen='Visual Studio 10 2010'
       elif sver[0]==15:
          cgen='Visual Studio 9 2008'
       elif sver[0]==14:
          cgen='Visual Studio 8 2005'
       elif sver[0]==13:
          cgen='Visual Studio 7 .NET 2003'
       elif sver[0]==12:
          cgen='Visual Studio 7'
       elif sver[0]==11:
          cgen='Visual Studio 6'

       if cgen!='':
          if str(tbits)=='64':
             cgen+=' Win64'

          env['CK_CMAKE_GENERATOR']=cgen

    if env.get('CK_CMAKE_GENERATOR','')=='':
       ck.out('**********************************')
       ck.out('Problem: can\'t detect Visual Studio compiler version from ('+str(sver)+')')
       ck.out('')
       ck.out('Please report to the authors at https://github.com/ctuning/ck-env/issues')
       ck.out('')
       r=ck.inp({'text':'Would you like to continue installation (Y/n): '})
       if r['return']>0: return r
       rx=r['string'].strip().lower()
       if rx=='n' or rx=='no': 
          return {'return':1, 'error':'can\'t detect Visual Studio compiler version'}

    ############################################################
    s+='\n'
    s+='rem Saving working path since next call can change it\n'
    s+='set CUR_DIR=%CD%\n'

    s+='\n'
    s+='rem Cleaning previous environment (to avoid conflicts if calling it several times during compilation)\n'
    s+='\n'
    s+='set "VCINSTALLDIR="\n'
    s+='set "VSINSTALLDIR="\n'

    s+='\n'
    s+='rem Setting environment\n'

    s+='call "'+fp+'" '+ext+'\n\n'

    s+='rem Restoring working path\n'
    s+='cd /D %CUR_DIR%\n'
    s+='\n'

    env['VSINSTALLDIR']=pi

    pix=pi
    if os.path.basename(pi)=='Auxiliary':
       pix=os.path.dirname(pix)

    # Try to get redistribute number VCxyz
    r=ck.access({'action':'list_all_files',
                 'module_uoa':'soft',
                 'path':pix, 
                 'pattern':'Microsoft.VC*.CRT',
                 'recursion_level_max':4})
    if r['return']>0: return r
    x=r['list']

    vc=''

    for q in x:
       j1=q.find('Microsoft.VC')
       if j1>=0:
          j2=q.find('.CRT',j1+1)
          if j2>0:
             vc=q[j1+12:j2]
             break

    env[ep+'_VC_MSBUILD']=vc

    env['CK_COMPILER_TOOLCHAIN_NAME']='msvc'

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

       env['VCINSTALLDIR']=os.path.dirname(pcl)

    return {'return':0, 'bat':s}
