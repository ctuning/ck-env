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
# customize directories to automatically find and register software

def dirs(i):
    import copy

    hosd=i.get('host_os_dict',{})
    tosd=i.get('target_os_dict',{})

    phosd=hosd.get('ck_name','')
    hbits=hosd.get('bits','')

    ptosd=tosd.get('ck_name','')

    lst=i['dirs']
    dirs=lst

    if ptosd=='win':
       for p in copy.deepcopy(lst):
           dirs.append(os.path.join(p, 'NVIDIA GPU Computing Toolkit\\CUDA'))

    return {'return':0, 'dirs':dirs}

##############################################################################
# get version from path

def version_cmd(i):

    ck=i['ck_kernel']

    ver=''
    fp=i['full_path']

    if fp!='':
       pl=os.path.dirname(fp)
       pl1=os.path.dirname(pl)
       pl2=os.path.dirname(pl1)

       pi=os.path.join(pl1,'include','cudnn.h')
       if not os.path.isfile(pi):
          pi=os.path.join(pl2,'include','cudnn.h')
       if os.path.isfile(pi):
          r=ck.load_text_file({'text_file':pi, 'split_to_list':'yes'})
          if r['return']==0:
             ll=r['lst']
             v1=''
             v2=''
             v3=''
             for l in ll:
                 if l.startswith('#define CUDNN_MAJOR'):
                    v1=l[19:].strip()
                 elif l.startswith('#define CUDNN_MINOR'):
                    v2=l[19:].strip()
                 elif l.startswith('#define CUDNN_PATCHLEVEL'):
                    v3=l[25:].strip()
                    break

             ver=v1+'.'+v2+'.'+v3

    if ver=='':
       fn=os.path.basename(fp)

       rfp=os.path.realpath(fp)
       rfn=os.path.basename(rfp)

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

    ############################################################
    # Setting environment depending on the platform
    if hplat=='win':
       pl=''
       pinc=''

       if fp!='':
          pl=os.path.dirname(fp)
          cus['path_lib']=pl

          pl1=os.path.dirname(pl)
          pl2=os.path.dirname(pl1)

          pi=''
          if os.path.isfile(os.path.join(pl1,'include','cudnn.h')):
             pi=pl1
          elif os.path.isfile(os.path.join(pl2,'include','cudnn.h')):
             pi=pl2

       pb=''

       se=cus.get('skip_ext','')

       # if Windows + CUDA
       if remote=='yes': 
          return {'return':1, 'error':'this software doesn\'t support Android'}
       else:
          ext='x64'
          if tbits=='32': 
             ext='Win32'

          pb=pi+'\\bin'
          if pl=='':
             pl=pi+'\\lib\\'+ext

       if pb!='': cus['path_bin']=pb
       if pl!='': cus['path_lib']=pl
       if pi!='': cus['path_include']=pi+'\\include'

       if remote=='yes': 
          cus['dynamic_lib']='cudnn.so'
       else:
          cus['static_lib']='cudnn.lib'

       cus['include_name']='cudnn.h'

    else:
       ### Linux ###
       lb=os.path.basename(fp)
       if lb=='': lb='libcudnn.so'

       pl=os.path.dirname(fp)
       cus['path_lib']=pl

       pl1=os.path.dirname(pl)
       pl2=os.path.dirname(pl1)

       pb=''
       if os.path.isdir(os.path.join(pl1,'bin')):
          pb=pl1
       elif os.path.isdir(os.path.join(pl2,'bin')):
          pb=pl2

       if pb!='':
          cus['path_bin']=os.path.join(pb,'bin')

       pi=''
       if os.path.isfile(os.path.join(pl1,'include','cudnn.h')):
          pi=pl1
       elif os.path.isfile(os.path.join(pl2,'include','cudnn.h')):
          pi=pl2

       if pi=='':
          if os.path.isfile('/usr/include/cudnn.h'):
             pi='/usr'
          elif os.path.isfile('/usr/local/include/cudnn.h'):
             pi='/usr/local'

       if pi!='':
          cus['path_include']=os.path.join(pi,'include')
          cus['include_name']='cudnn.h'

       cus['static_lib']=lb
       cus['dynamic_lib']=lb

       r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': hosd, 
         'lib_path': cus.get('path_lib','')})
       if r['return']>0: return r
       s += r['script']

    ep=cus.get('env_prefix','')
    if pi!='' and ep!='':
       env[ep]=pi

       rx=ck.access({'action':'convert_to_cygwin_path',
                     'module_uoa':'os',
                     'path':pi})
       if rx['return']>0: return rx
       env[ep+'_WIN']=rx['path']

    if remote=='yes':
       cus['skip_copy_to_remote']='yes'

    env[ep+'_INCLUDE_NAME']=cus.get('include_name','')
    env[ep+'_STATIC_NAME']=cus.get('static_lib','')
    env[ep+'_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    return {'return':0, 'bat':s}
