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
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    if len(lst)>0:
       ver=lst[0].strip()

       j1=ver.find(' EasyBuild ')
       if j1>0:
          j2=ver.find('(', j1)
          if j2>0:
             ver=ver[j1+11:j2].strip()

    return {'return':0, 'version':ver}

##############################################################################
# setup environment

def setup(i):

    s=''

    cus=i['customize']
    env=i['env']

    fp=cus.get('full_path','')

    ep=cus['env_prefix']
    if fp!='':
       p1=os.path.dirname(fp)
       p2=os.path.dirname(p1)
       p3=os.path.dirname(p2)
       p4=os.path.dirname(p3)
       p5=os.path.dirname(p4)

       env[ep]=p2
       env[ep+'_BIN']=p1
       env[ep+'_ROOT']=p5
       env['EASYBUILD_PREFIX']=p5

    return {'return':0, 'bat':s}
