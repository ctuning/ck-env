#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: dividiti
#

import os

##############################################################################
# customize directories to automatically find and register software

def dirs(i):
    dirs=i.get('dirs', [])
    for d in extra_dirs:
        if os.path.isdir(d):
            dirs.append(d)
    return {'return':0, 'dirs':dirs}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

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

       env['TVM_HOME']=p2
       env['PYTHONPATH'] = p2 + '/python:${PYTHONPATH}'

    return {'return':0, 'bat':s}
