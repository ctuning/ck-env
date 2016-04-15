#
# Collective Knowledge (scripts and tools to initialize a given platform)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# select and set platform.init scripts

def set(i):
    """
    Input:  {
              (host_os)              - host OS (detect, if omitted)
              (os) or (target_os)    - OS module to check (if omitted, analyze host)

              (device_id)            - device id if remote (such as adb)

              (data_uoa)             - force platform init uoa
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    o=i.get('out','')

    duoa=i.get('data_uoa','')

    # First, check if it is already in kernel cfg
    pi_uoa=cfg.get('platform_init_uoa','')
    if pi_uoa=='':
       if duoa!='':
          pi_uoa=duoa
       elif os.environ.get('CK_PLATFORM_INIT_UOA','')!='':
          pi_uoa=os.environ['CK_PLATFORM_INIT_UOA']
       else:
          # Attempt to detect
          hos=i.get('host_os','')
          tos=i.get('target_os','')
          if tos=='': tos=i.get('os','')
          tdid=i.get('device_id','')

          # Get OS info ##############################################################
          ii={}
          ii['action']='detect'
          ii['module_uoa']=cfg['module_deps']['platform.os']

          rr=ck.access(ii) # DO NOT USE rr further - will be reused as return !
          if rr['return']>0: return rr

          hos=rr['host_os_uid']
          hosx=rr['host_os_uoa']
          hosd=rr['host_os_dict']

          tos=rr['os_uid']
          tosx=rr['os_uoa']
          tosd=rr['os_dict']

          tbits=tosd.get('bits','')

          tdid=rr['device_id']

          prop=rr['features']['os']


          print ('xyz')




    # Selected


    return {'return':0}
