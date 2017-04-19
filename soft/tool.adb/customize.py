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
    xdirs=i.get('dirs', [])

    x=ck.work['dir_repos']
    if x!='': 
       x=os.path.join(x,'ck-env')
       xdirs.append(x)

    return {'return':0, 'dirs':xdirs}

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
        if q!='':
           j=q.lower().find('version ')
           if j>0:
              ver=q[j+8:]
              break

    return {'return':0, 'version':ver}

##############################################################################
# setup environment

def setup(i):

    s=''

    cus=i['customize']
    env=i['env']

    fp=cus.get('full_path','')

    ep=cus.get('env_prefix','')
    if ep!='' and fp!='':
       p1=os.path.dirname(fp)
       p2=os.path.dirname(p1)

       env[ep]=p2
       env[ep+'_BIN']=p1

    return {'return':0, 'bat':s}
