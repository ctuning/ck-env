#
# Collective Knowledge (APK entries)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: cTuning foundation, admin@cTuning.org, http://cTuning.org
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings
import os

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
# detect installed APKs

def detect(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    # Check if need to initialize device and directly update input i !
    ii={'action':'init',
        'module_uoa':cfg['module_deps']['machine'],
        'input':i}
    r=ck.access(ii)
    if r['return']>0: return r

    device_cfg=i.get('device_cfg',{})

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('device_id','')

    # Get some info about platforms
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.os'],
        'host_os':hos,
        'target_os':tos,
        'device_cfg':device_cfg,
        'device_id':tdid,
        'skip_info_collection':'yes'}
    r=ck.access(ii)
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    tdid=i.get('device_id','')

    xtdid=''
    if tdid!='': xtdid=' -s '+tdid

    env_sep=hosd.get('env_separator','')

    x='"'

    adb=tosd['remote_shell'].replace('$#device#$',xtdid)+' '+x+'pm list packages -f'+x

    # ADB dependency
    deps={'adb':{
                 "force_target_as_host": "yes",
                 "local": "yes", 
                 "name": "adb tool", 
                 "sort": -10, 
                 "tags": "tool,adb"
                 }
         }

    ii={'action':'resolve',
        'module_uoa':cfg['module_deps']['env'],
        'host_os':hos,
        'target_os':tos,
        'device_id':tdid,
        'deps':deps,
        'add_customize':'yes',
        'out':oo}
    rx=ck.access(ii)
    if rx['return']>0: return rx

    s=rx['cut_bat'].strip()+' '+env_sep+' '+adb

    print (s)
    os.system(s)




    return {'return':0}
