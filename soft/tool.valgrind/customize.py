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

    print (lst)

    ver=''
    if len(lst)>0:
        x=lst[0]

        if x.startswith('valgrind-'):
            ver=x[9:].strip()

    return {'return':0, 'version':ver}

##############################################################################
# setup environment

def setup(i):

    s=''

    cus=i['customize']
    env=i['env']

    host_d=i.get('host_os_dict',{})
    target_d=i.get('host_os_dict',{})

    tbits=target_d.get('bits','')

    winh=host_d.get('windows_base','')

    # Get paths
    fp=cus['full_path']
    ep=cus['env_prefix']

    pn=os.path.basename(fp)

    env[ep+'_TOOL']=pn
    env[ep+'_FTOOL']=fp

    p1=os.path.dirname(fp)
    p2=os.path.dirname(p1)

    env[ep]=p2
    env[ep+'_BIN']=p1

    return {'return':0, 'bat':s}
