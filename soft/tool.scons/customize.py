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
    for x in lst:
       j=x.find('engine: v')
       if j>=0:
           ver=x[j+9:].strip()

           j=ver.find('.rel')
           if j>0:
              ver=ver[:j]

           break

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

    pb=os.path.dirname(fp)
    p2=os.path.dirname(pb)

    env[ep]=p2
    env[ep+'_BIN']=pb

    return {'return':0, 'bat':s}
