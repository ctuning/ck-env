#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os

extra_dirs=['C:\\Strawberry', 'D:\\Strawberry',
            'C:\\Perl64', 'D:\\Perl64',
            'C:\\Perl', 'D:\\Perl']

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

    for q in lst:
        q=q.strip().lower()
        if q!='' and q.startswith('this is perl'):
           j1=q.find('(')
           if j1>0:
              j2=q.find(')',j1+1)
              if j2>0:
                 ver=q[j1+1:j2]

           break

    if ver!='' and ver.startswith('v'):
       ver=ver[1:]

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
