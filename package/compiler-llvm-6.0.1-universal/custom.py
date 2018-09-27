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

              (install_env) - prepare environment to be used before the install script
            }

    """

    import os
    import shutil

    # Get variables
    o=i.get('out','')

    ck=i['ck_kernel']

    hos=i['host_os_uoa']
    tos=i['target_os_uoa']

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    hbits=hosd.get('bits','')
    tbits=tosd.get('bits','')

    hname=hosd.get('ck_name','')    # win, linux
    hname2=hosd.get('ck_name2','')  # win, mingw, linux, android
    macos=hosd.get('macos','')      # yes/no

    hft=i.get('features',{}) # host platform features
    habi=hft.get('os',{}).get('abi','') # host ABI (only for ARM-based); if you want to get target ABI, use tosd ...
                                        # armv7l, etc...

    p=i['path']

    env=i['env']

    pi=i.get('install_path','')

    cus=i['customize']
    ie=cus.get('install_env',{})
    nie={} # new env

    # Update vars
    if macos=='yes':
       return {'return':1, 'error':'MacOS is not supported yet'}
#       if hbits!='64':
#          return {'return':1, 'error':'this package doesn\'t support non 64-bit MacOS'}

#       nie['PACKAGE_NAME']='clang+llvm-6.0.1-x86_64-apple-darwin.tar.xz'

#       nie['PACKAGE_UNXTAR']='YES'
#       nie['PACKAGE_UNTAR_EXTRA']='--strip 1'
#       nie['PACKAGE_SKIP_LINUX_MAKE']='YES'

    elif hname=='win':
       f='LLVM-6.0.1-win'
       if hbits=='64':
          f+='64.exe'
       else:
          f+='32.exe'

       nie['PACKAGE_NAME']=f
       nie['PACKAGE_WGET_EXTRA']=ie['PACKAGE_WGET_EXTRA']+' -O '+f
       nie['PACKAGE_RUN']='YES'

       ck.out('')
       ck.out('WARNING: Please copy the following path and then paste it when LLVM will ask you about installation path!')
       ck.out('')
       ck.out(pi)
       ck.out('')
       ck.inp({'text':'Press Enter to continue!'})

    else:
       if habi.startswith('arm') or habi.startswith('aarch'):
#          return {'return':1, 'error':'ARM platform is not supported yet'}
          if hbits=='64':
             nie['PACKAGE_NAME']='clang+llvm-6.0.1-aarch64-linux-gnu.tar.xz'
          else:
             nie['PACKAGE_NAME']='clang+llvm-6.0.1-armv7a-linux-gnueabihf.tar.xz'
       else:
          r=ck.access({'action':'detect','module_uoa':'platform.os', 'out':o})
          if r['return']>0: return r

          flavor=r.get('features',{}).get('os',{}).get('name','').lower()

          ver=''
          mver=''
          x=flavor.split(' ')
          if len(x)>1:
             ver=x[1]
             mver=ver
             j=ver.find('.')
             if j>=0:
                j1=ver.find('.',j+1)
                if j1>=0:
                   mver=ver[:j1]

          if 'debian' in flavor:
             return {'return':0, 'error':'debian is not supported yet'}
#             nie['PACKAGE_NAME']='clang+llvm-6.0.1-x86_64-linux-gnu-debian8.tar.xz'
          else:
             nie['PACKAGE_NAME']='clang+llvm-6.0.1-x86_64-linux-gnu-ubuntu-16.04.tar.xz'

             if mver=='14.04':
                nie['PACKAGE_NAME']='clang+llvm-6.0.1-x86_64-linux-gnu-ubuntu-14.04.tar.xz'
             elif mver=='16.10':
                nie['PACKAGE_NAME']='clang+llvm-6.0.1-x86_64-linux-gnu-ubuntu-16.04.tar.xz'

       nie['PACKAGE_UNXTAR']='YES'
       nie['PACKAGE_UNTAR_EXTRA']='--strip 1'
       nie['PACKAGE_SKIP_LINUX_MAKE']='YES'

    return {'return':0, 'install_env':nie}
