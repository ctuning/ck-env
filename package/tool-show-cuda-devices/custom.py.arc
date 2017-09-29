#!/usr/bin/python

#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os
import sys
import json

##############################################################################
# customize installation

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet

              path             - path to entry (with scripts)
              install_path     - installation path
            }

    Output: {
              return        - return code =  0, if successful
                                          >  0, if error
              (error)       - error text if return > 0
              (install-env) - prepare environment to be used before the install script
            }

    """

    import os
    import shutil

    # Get variables
    o=i.get('out','')

    ck=i['ck_kernel']
    s=''

    hos=i['host_os_uoa']
    tos=i['target_os_uoa']

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    p=i['path']

    pi=i.get('install_path','')

    pib=os.path.join(pi,'bin')
    if not os.path.exists(pib):
        os.makedirs(pib)       

    rr={'return':0, 'soft_cfg':{}}

    # Try to compile program
    if o=='con':
        ck.out('Compiling tool via CK ...')

    r=ck.access({'action':'compile',
                 'module_uoa':'program',
                 'data_uoa':'tool-print-cuda-devices',
                 'host_os':hos,
                 'target_os':tos,
                 'out':o})
    if r['return']>0: return r

    misc=r.get('misc',{})

    if misc.get('compilation_success','')!='yes':
        return {'return':1, 'error':'compilation failed'}

    texe=misc['target_exe']

    texe1=texe
    if texe1.endswith('.out'):
        texe1=texe1[:-4]
    if texe1.startswith('ck-'):
        texe1=texe1[3:]

    # Prepare full path to the newly created binary
    p=misc['path']
    if misc.get('tmp_dir','')!='':
        p=os.path.join(p,misc['tmp_dir'])
    p=os.path.join(p,texe)

    # Check deps
    deps=r.get('deps',{})
    if len(deps)>0:
        rr['soft_cfg']['deps']=deps

    # Prepare target path
    pt=os.path.join(pib, texe1)

    # Copy file
    if o=='con':
       ck.out('')
       ck.out('Copying file '+p+' to '+pt+' ...')
       ck.out('')

    try:
        shutil.copyfile(p,pt)
    except Exception as e: 
        return {'return':1, 'error':'Copying file to installation directory failed'}

    # Check if need to set executable
    se=hosd.get('set_executable','')
    if se!='':
       se+=' '+pt

       os.system(se)

    rr['soft_cfg']['skip_device_info_collection']='yes'

    return rr
