#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK Copyright.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://cTuning.org/lab/people/gfursin
#

##############################################################################
# setup environment setup

import sys
if sys.version_info[0]>2:
   def raw_input(i):
       return input(i)

def setup(i):
    """
    Input:  {
              cfg          - dict of the soft entry
              tags         - list of tags
              env          - environment
              deps         - resolved deps

              interactive  - if 'yes', ask questions

              (customize)  - external params for possible customization:

                             target_arm - if 'yes', target ARM
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat        - prepared string for bat file
            }

    """

    import os

    # Get variables
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

          x=raw_input('Do you target ARM processors (Y/n): ')
          if x!='' and x!='Y' and x!='yes': 
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
          print ('')
          if x=='':
             x=raw_input('Input path to Windows SDK (example: C:\\Program Files (x86)\\Microsoft SDKs\\Windows\\v7.1A"): ')
          else:
             print ('Current Windows SDK path: '+x)
             x=raw_input('Input new path to Windows SDK (or press Enter to keep the same): ')

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
