#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

##############################################################################
# setup environment setup

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
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    import os

    # Get variables
    ck=i['ck_kernel']
    s=''

    iv=i.get('interactive','')

    env=i.get('env',{})
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})
    tags=i.get('tags',[])
    cus=i.get('customize',{})

    target_d=i.get('target_os_dict',{})
    win=target_d.get('windows_base','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    ############################################################
    s+='\n'
    s+='rem Setting environment\n'

    yy='call "'+pi+'\\vcvarsall.bat" '

    # Check which processor
    arm=cus.get('target_arm','')
    if target_d.get('remote','')=='yes' and arm=='':
       arm='yes'
       if iv=='yes':
          ck.out('You selected remote platform as a target.')

          ra=ck.inp({'text':'Do you target ARM processors (Y/n): '})
          x=ra['string'].strip().lower()
          if x!='' and x!='y' and x!='yes': 
             arm='no'

    if arm=='yes':
       yy+=' x86_arm'
    else:
       if tbits=='32': yy+=' x86'
       else: yy+=' amd64'

    s+=yy+'\n\n'

    if cus.get('add_win_sdk_path','')=='yes':
       if iv=='yes':
          x=cus.get('CK_WINDOWS_SDK_PATH','')
          ck.out('')
          if x=='':
             ra=ck.inp({'text':'Input path to Windows SDK (example: C:\\Program Files (x86)\\Microsoft SDKs\\Windows\\v7.1A"): '})
             x=ra['string'].strip()
          else:
             ck.out('Current Windows SDK path: '+x)
             ra=ck.inp({'text':'Input new path to Windows SDK (or press Enter to keep the same): '})
             x=ra['string'].strip()

          if x!='': 
             env['CK_WINDOWS_SDK_PATH']=x
             cus['CK_WINDOWS_SDK_PATH']=x

       x=cus.get('CK_WINDOWS_SDK_PATH','')
       if x!='':
          y=x+'\\'
          if tbits=='32': y+='Lib'
          else: y+='Lib\\'+'x64'
          s+='set LIB='+y+';%LIB%\n\n'

    return {'return':0, 'bat':s}
