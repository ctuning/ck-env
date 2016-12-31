#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os
import sys

##############################################################################
# limit directories 

def limit(i):

    hosd=i.get('host_os_dict',{})
    tosd=i.get('target_os_dict',{})

    tbits=tosd.get('bits','')

    phosd=hosd.get('ck_name','')
    ext=''
    if tbits=='64':
       ext='x64'

    dr=i.get('list',[])
    drx=[]

    for q in dr:                                                               
        if (tbits=='64' and q.find('x64')>0) or (tbits=='32' and q.find('x64')<0):
           drx.append(q)

    return {'return':0, 'list':drx}

##############################################################################
# get version from path

def version_cmd(i):

    ck=i['ck_kernel']

    fp=i['full_path']

    ver=''

    p1=os.path.dirname(fp)
    p2=os.path.dirname(p1)
    p3=os.path.dirname(p2)

    fv=os.path.join(p2,'Readme.txt')
    if not os.path.isfile(fv):
       fv=os.path.join(p3,'Readme.txt')
    if os.path.isfile(fv):
       rx=ck.load_text_file({'text_file':fv, 'split_to_list':'yes', 'encoding':sys.stdin.encoding})
       if rx['return']==0:
          lst=rx['lst']
          for q in lst:
              if q.lower().startswith('freeglut '):
                 ver=q[9:]
                 j=ver.find(' ')
                 if j>=0:
                    ver=ver[:j]
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

    host_d=i.get('host_os_dict',{})
    sdirs=host_d.get('dir_sep','')

    fp=cus.get('full_path','')

    pl=os.path.dirname(fp)
    ext=os.path.basename(pl)
    if ext!='x64': ext=''

    pi=fp
    found=False
    while True:
       if os.path.isdir(os.path.join(pi,'include')):
          found=True
          break
       pix=os.path.dirname(pi)
       if pix==pi:
          break
       pi=pix

    if tbits=='64' and os.path.isdir(os.path.join(pl,'x64')):
       pl=os.path.join(pl,'x64')

    cus['path_lib']=pl
    cus['path_include']=pi+sdirs+'include'

    ep=cus['env_prefix']
    env[ep]=pi
    env[ep+'_LIB']=pl

    ################################################################
    if win=='yes':
       pb=pi+'\\bin'
       if ext!='':
          pb+='\\'+ext

       if tbits=='64' and os.path.isdir(os.path.join(pb,'x64')):
          pb=os.path.join(pb,'x64')

       s+='set PATH='+pb+';%PATH%\n\n'
       env[ep+'_BIN']=pb
    else:
       return {'return':1, 'error':'Linux version is not yet supported in customize.py'}

    return {'return':0, 'bat':s}
