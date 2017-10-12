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
# setup environment

def setup(i):

    s=''

    cus=i['customize']
    env=i['env']

    fp=cus['full_path']

    ep=cus['env_prefix']

    host_d=i.get('host_os_dict',{})
    winh=host_d.get('windows_base','')

    p1=os.path.dirname(fp)
    p2=os.path.dirname(p1)
    p3=os.path.dirname(p2)

    env[ep]=p3
    env[ep+'_LIB']=p2

    if winh=='yes':
        s+='\nset PYTHONPATH='+p2+';%PYTHONPATH%\n'
    else:
        s+='\nexport PYTHONPATH='+p2+':${PYTHONPATH}\n'

    return {'return':0, 'bat':s}
