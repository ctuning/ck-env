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

    return {'return':0, 'version':'default'}

##############################################################################
# setup environment

def setup(i):

    s=''

    cus=i['customize']
    env=i['env']

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    hplat=hosd.get('ck_name','')

    target_d=i.get('target_os_dict',{})
    winh=hosd.get('windows_base','')

    fp=cus.get('full_path','')

    ep=cus['env_prefix']

    p1=os.path.dirname(fp)
    pi=os.path.dirname(p1)

    p2pt=os.path.join(pi,'platform-tools')
    p2p=os.path.join(pi,'platforms')
    p2s=os.path.join(pi,'sources')
    p2t=os.path.join(pi,'tools')

    env[ep]=pi
    env[ep+'_BIN']=p2t
    env[ep+'_TOOLS']=p2t
    env[ep+'_PLATFORMS']=p2p
    env[ep+'_SOURCES']=p2s
    env[ep+'_PLATFORM_TOOLS']=p2pt

    # Need to set ANDROID_HOME
    s+='\n'
    if winh=='yes':
        s+='set ANDROID_HOME='+pi
    else:
        s+='export ANDROID_HOME='+pi
    s+='\n\n'

    return {'return':0, 'bat':s}
