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
              (name) - get params only for this APK
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

    # Check remote shell
    rs=tosd.get('remote_shell','')
    if rs=='':
        return {'return':1, 'error':'APK are not supported for this target'}

    tdid=i.get('device_id','')

    xtdid=''
    if tdid!='': xtdid=' -s '+tdid

    envsep=hosd.get('env_separator','')
    sext=hosd.get('script_ext','')
    sexe=hosd.get('set_executable','')
    sbp=hosd.get('bin_prefix','')
    scall=hosd.get('env_call','')
    ubtr=hosd.get('use_bash_to_run','')

    x='"'

    # Record to tmp batch and run
    rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':'.tmp', 'remove_dir':'no'})
    if rx['return']>0: return rx
    fnx=rx['file_name']

    adb=rs.replace('$#device#$',xtdid)+' '+x+'pm list packages'+x+' > '+fnx

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
    sbb=rx['cut_bat']

    sb=sbb+'\n'+adb

    # Record to tmp batch and run
    rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':sext, 'remove_dir':'no'})
    if rx['return']>0: return rx
    fn=rx['file_name']

    rx=ck.save_text_file({'text_file':fn, 'string':sb})
    if rx['return']>0: return rx

    y=''
    if sexe!='':
       y+=sexe+' '+fn+envsep
    y+=' '+scall+' '+fn

    if ubtr!='': y=ubtr.replace('$#cmd#$',y)
    os.system(y)

    if os.path.isfile(fn):
        os.remove(fn)

    # Reading file
    rx=ck.load_text_file({'text_file':fnx, 'split_to_list':'yes', 'delete_after_read':'yes'})
    if rx['return']>0: return rx
    lst=rx['lst']

    params={}

    name=i.get('name','')

    iapk=0
    for package in lst:
        if package.startswith('package:'):
            package=package[8:]

        if name!='' and package!=name:
            continue

        iapk+=1
        ck.out(package)

        params[package]={}

        # Get parameters
        sb=sbb+'\n'+rs.replace('$#device#$',xtdid)+' '+x+'dumpsys package '+package+x+' > '+fnx

        rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':sext, 'remove_dir':'no'})
        if rx['return']>0: return rx
        fn=rx['file_name']

        rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':sext, 'remove_dir':'no'})
        if rx['return']>0: return rx
        fny=rx['file_name']

        rx=ck.save_text_file({'text_file':fn, 'string':sb})
        if rx['return']>0: return rx

        y=''
        if sexe!='':
           y+=sexe+' '+fn+envsep
        y+=' '+scall+' '+fn+' > '+fny

        if ubtr!='': y=ubtr.replace('$#cmd#$',y)
        os.system(y)

        if os.path.isfile(fn):
            os.remove(fn)

        if os.path.isfile(fny):
            os.remove(fny)

        # Reading file
        rx=ck.load_text_file({'text_file':fnx, 'split_to_list':'yes', 'delete_after_read':'yes'})
        if rx['return']>0: return rx
        ll=rx['lst']

        for q in ll:
            j=q.find('=')
            if j>0:
                j1=q.rfind(' ', 0, j)
                k=q[j1+1:j]
                v=q[j+1:]

                j2=v.find(' targetSdk=')
                if j2>0:
                    vv=v[j2+11:]
                    v=v[:j2]
                    kk='targetSdk'

                    params[package][kk]=vv

                params[package][k]=v

    if name!='':
        if iapk==0:
            return {'return':1, 'error':'APK was not found on the target device'}

        if o=='con':
            ck.out('')
            ck.out('Parameters:')
            ck.out('')

            for k in sorted(params[name]):
                v=params[name][k]
                ck.out('  '+k+' = '+v)
    return {'return':0, 'params':params}
