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
              (name)      - get params only for this APK
              (target_os) - target Android OS (ck search os --tags=android)
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

    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('device_id','')
    target=i.get('target','')

    ii={'action':'shell',
        'module_uoa':cfg['module_deps']['os'],
        'host_os':hos,
        'target_os':tos,
        'device_id':tdid,
        'target':target,
        'split_to_list':'yes',
        'cmd':'pm list packages'}

    r=ck.access(ii)
    if r['return']>0: return r

    tosd=r['target_os_dict']

    lst=r['stdout_lst']

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
        ii={'action':'shell',
            'module_uoa':cfg['module_deps']['os'],
            'host_os':hos,
            'target_os':tos,
            'device_id':tdid,
            'target':target,
            'split_to_list':'yes',
            'cmd':'dumpsys package '+package}

        r=ck.access(ii)
        if r['return']>0: return r

        ll=r['stdout_lst']

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
            return {'return':16, 'error':'APK was not found on the target device'}

        if o=='con':
            ck.out('')
            ck.out('Parameters:')
            ck.out('')

            for k in sorted(params[name]):
                v=params[name][k]
                ck.out('  '+k+' = '+v)
    return {'return':0, 'params':params, 'target_os_dict':tosd}

##############################################################################
# check APK

def check(i):
    """
    Input:  {
              (host_os)
              (target_os)
              (device_id)

              name        - APK name
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    name=i.get('name','')
    if name=='':
        return {'return':1, 'error':'APK "name" is not defined'}

    rr={'return':0}

    # Detect if APK is installed
    r=detect(i)
    if r['return']>0 and r['return']!=16: return r

    if r['return']==16:
        # APK is not installed
        tosd=r['target_os_dict']

        abi=tosd.get('abi','')

        # Check if available in the CK
        r=ck.access({'action':'load',
                     'module_uoa':work['self_module_uid'],
                     'data_uoa':name})
        if r['return']>0 and r['return']!=16: return r

        found=False
        if r['return']==0:
            p=r['path']
            d=r['dict']

            dabi=d.get(abi,{})

            aname=dabi.get('apk_name','')

            if aname!='':
                pp=os.path.join(p, abi, aname)

                if os.path.isfile(pp):
                    # Trying to install
                    print ('abc')

        # If not found

        print ('xyz')

    rr['params']=r['params']

    return rr
