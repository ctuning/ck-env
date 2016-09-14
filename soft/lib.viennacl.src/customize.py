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

  # Get updated environment and customized variables.
  env=i.get('env',{})
  cus=i.get('customize',{})

  # FIXME: pi=cus.get('path_install','') - does not seem to work,
  # hence the ugly workround.
  fp=cus.get('full_path','')
  pi=os.path.dirname(os.path.dirname(fp)) # ../..

  ep=cus.get('env_prefix','')
  if pi!='' and ep!='':
    env[ep]=pi
  cus['path_include']=pi

  return {'return':0,'bat':''}
