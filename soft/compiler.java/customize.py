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
    return {'return':0}

##############################################################################
# limit directories 

def limit(i):

    dr=i.get('list',[])
    drx=[]

    for q in dr:
        if q.find('X11')<0:
           drx.append(q)

    return {'return':0, 'list':drx}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip()
        if q!='' and q.startswith('javac') and len(q)>5:
           ver=q[6:]
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
       return {'return':1, 'error':'full path to java compiler required by soft customization script is empty'}

    p1=os.path.dirname(fp)
    p2=os.path.dirname(p1)

    env[ep]=p2
    env[ep+'_BIN']=p1

    env['JAVA_HOME']=p2

    return {'return':0, 'bat':s}
