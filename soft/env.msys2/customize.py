#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os

extra_dirs=['C:\\msys64', 'C:\\tools\\msys2', 'D:\\msys64', 'D:\\tools\\msys2']

##############################################################################
# customize directories to automatically find and register software

def dirs(i):

    hosd=i['host_os_dict']
    phosd=hosd.get('ck_name','')
    dirs=i.get('dirs', [])

    if phosd=='win':
        for d in extra_dirs:
            if os.path.isdir(d):
                dirs.append(d)

    return {'return':0, 'dirs':dirs}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip()
        if q!='':
           j=q.lower().find('version ')
           if j>0:
              ver=q[j+8:].strip()

              j2=ver.find(' ')
              if j2>0:
                 ver=ver[:j2]

              ver=ver.strip()
              
              break

    return {'return':0, 'version':ver}

##############################################################################
# setup environment

def setup(i):

    s=''

    cus=i['customize']
    env=i['env']

    fp=cus.get('full_path','')

    ep=cus['env_prefix']

    if fp=='':
       return {'return':1, 'error':'full path required by the soft customization script is empty'}

    p1=os.path.dirname(fp)
    p2=os.path.dirname(p1)
    p3=os.path.dirname(p2)

    env[ep]=p3
    env[ep+'_BIN']=p1

    env[ep+'_BASH']=fp

    return {'return':0, 'bat':s}
