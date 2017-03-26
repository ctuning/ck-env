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
        x=lst[0]

        if x.startswith('Build label:'):
            ver=x[12:].strip()

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

    px=os.path.join(p2,'bazel-bin','scripts','bazel-complete.bash')
    if os.path.isfile(px):
       env[ep+'_INIT']=px

       if winh!='yes':
          s+='\nsource '+px+'\n\n'

    env[ep]=p2
    env[ep+'_BIN']=pb

    if winh=='yes':
       env['BAZEL_SH']='%CK_ENV_MSYS2_BASH%'

    return {'return':0, 'bat':s}
