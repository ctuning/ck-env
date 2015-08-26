#
# Collective Knowledge (platform detection)
#
# See CK LICENSE.txt for licensing details
# See CK Copyright.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://cTuning.org/lab/people/gfursin
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings
sep='***************************************************************************************'

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
# collect info about platforms

def detect(i):
    """
    Input:  {
              (host_os)              - host OS (detect, if omitted)
              (os) or (target_os)    - OS module to check (if omitted, analyze host)

              (device_id)            - device id if remote (such as adb)
              (skip_device_init)     - if 'yes', do not initialize device
              (print_device_info)    - if 'yes', print extra device info

              (skip_info_collection) - if 'yes', do not collect info (particularly for remote)

              (exchange)             - if 'yes', exchange info with some repo (by default, remote-ck)
              (share)                - the same as 'exchange'
              (exchange_repo)        - which repo to record/update info (remote-ck by default)
              (exchange_subrepo)     - if remote, remote repo UOA

              (force_platform_name)  - if !='', use this for platform name
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              host_os_uoa                 - host OS UOA
              host_os_uid                 - host OS UID
              host_os_dict                - host OS meta

              os_uoa                      - target OS UOA
              os_uid                      - target OS UID
              os_dict                     - target OS meta

              (devices)                   - return devices if device_id==''
              (device_id)                 - if device_id=='' and only 1 device, select it

              features = {
                cpu            - CPU features (properties), unified
                cpu_misc       - assorted CPU features (properties), platform dependent

                os             - OS features (properties), unified
                os_misc        - assorted OS features (properties), platform dependent

                platform       - platform features (properties), unified
                platform_misc  - assorted platform features (properties), platform dependent

                acc            - Accelerator features (properties), unified
                acc_misc       - assorted Accelerator features (properties), platform dependent
              }
            }

    """

    import os

    o=i.get('out','')

    oo=''
    if o=='con': oo=o

    # Various params
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    if tos=='': tos=i.get('os','')
    tdid=i.get('device_id','')

    sic=i.get('skip_info_collection','')
    sdi=i.get('skip_device_init','')
    pdv=i.get('print_device_info','')
    ex=i.get('exchange','')
    if ex=='': ex=i.get('share','')

    # If exchange, check that repo from this env is cached and recache if needed
    if ex=='yes':
       er=i.get('exchange_repo','')
       rx=ck.load_repo_info_from_cache({'repo_uoa':ex})
       if rx['return']>0: 
          if o=='con':
             ck.out('')
             ck.out('Adding repo from this "env" package to local cache ...')

          rx=ck.access({'action':'recache',
                        'module_uoa':cfg['module_deps']['repo']})
          if rx['return']>0: return rx

    # Get OS info ###############################################################
    if oo=='con': 
       ck.out(sep)
       ck.out('Detecting OS and CPU features ...')

    import copy
    ii=copy.deepcopy(i)
    ii['out']=oo
    ii['action']='detect'
    ii['module_uoa']=cfg['module_deps']['platform.cpu']
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

    # Some params
    ro=tosd.get('redirect_stdout','')
    remote=tosd.get('remote','')
    win=tosd.get('windows_base','')

    dv=''
    if tdid!='': dv=' -s '+tdid

    # Init
    prop={}
    prop_all={}

    xos=rr['os_uoa']
    device_id=rr['device_id']

    os_uoa=rr['os_uoa']
    os_uid=rr['os_uid']
    os_dict=rr['os_dict']

    remote=os_dict.get('remote','')
    os_win=os_dict.get('windows_base','')

    ro=os_dict.get('redirect_stdout','')

    # Get accelerator info (GPU, etc.) ####################################################
    if oo=='con': 
       ck.out(sep)
       ck.out('Detecting accelerator features ...')

    import copy
    ii=copy.deepcopy(i)
    ii['out']=oo
    ii['skip_print_os_info']='yes'
    ii['action']='detect'
    ii['module_uoa']=cfg['module_deps']['platform.accelerator']
    rx=ck.access(ii) # DO NOT USE rr further - will be reused as return !
    if rx['return']>0: return rr
    rr.update(rx)

    # Get info about system ######################################################
    if oo=='con': 
       ck.out(sep)
       ck.out('Detecting system features ...')

    remote=os_dict.get('remote','')
    if remote=='yes':
       params={}

       rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
       if rx['return']>0: return rx
       fn=rx['file_name']

       x=tosd.get('adb_all_params','')
       x=x.replace('$#redirect_stdout#$', ro)
       x=x.replace('$#output_file#$', fn)

       dv=''
       if tdid!='': dv=' -s '+tdid
       x=x.replace('$#device#$',dv)

       if o=='con' and pdv=='yes':
          ck.out('')
          ck.out('Receiving all parameters:')
          ck.out('  '+x)

       rx=os.system(x)
       if rx!=0:
          if o=='con':
             ck.out('')
             ck.out('Non-zero return code :'+str(rx)+' - likely failed')
          return {'return':1, 'error':'access to remote device failed'}

       # Read and parse file
       rx=ck.load_text_file({'text_file':fn, 'split_to_list':'yes', 'delete_after_read':'yes'})
       if rx['return']>0: return rx
       ll=rx['lst']

       for s in ll:
           s1=s.strip()

           q2=s1.find(']: [')
           k=''
           if q2>=0:
              k=s1[1:q2].strip()
              v=s1[q2+4:].strip()
              v=v[:-1].strip()

              params[k]=v

       prop_all['adb_params']=params

#       for q in params:
#           v=params[q]
#           print q+'='+v

       model=params.get('ro.product.model','')
       manu=params.get('ro.product.manufacturer','')
       if model!='' and manu!='':
          if model.lower().startswith(manu.lower()):
             model=model[len(manu)+1:]

       if manu=='' and model!='': manu=model
       prop['name']=manu
       if model!='': prop['name']+=' '+model
       prop['model']=model
       prop['vendor']=manu
    else:
       x1=''
       x2=''

       target_system_model=''
       target_name=''

       if os_win=='yes':
          r=get_from_wmic({'group':'csproduct'})
          if r['return']>0: return r
          info1=r['dict']

          x1=info1.get('Vendor','')
          x2=info1.get('Version','')

          target_name=x1+' '+x2

          r=get_from_wmic({'cmd':'computersystem get model'})
          if r['return']>0: return r
          target_system_model=r['value']

          prop_all['cs_product']=info1
       else:
          file_with_vendor='/sys/devices/virtual/dmi/id/sys_vendor'
          if os.path.isfile(file_with_vendor):
             r=ck.load_text_file({'text_file':file_with_vendor})
             if r['return']>0: return r
             x1=r['string'].strip()

          file_with_version='/sys/devices/virtual/dmi/id/product_version'
          if os.path.isfile(file_with_version):
             r=ck.load_text_file({'text_file':file_with_version})
             if r['return']>0: return r
             x2=r['string'].strip()

          if x1!='' and x2!='':
             target_name=x1+' '+x2

          file_with_id='/sys/devices/virtual/dmi/id/product_name'
          if os.path.isfile(file_with_id):
             r=ck.load_text_file({'text_file':file_with_id})
             if r['return']>0: return r
             target_system_model=r['string'].strip()

       prop['vendor']=x1
       if target_name=='' and x1!='': target_name=x1
       prop['name']=target_name
       if target_system_model!='': prop['name']+=' ('+target_system_model+')'
       prop['model']=target_system_model

       fpn=i.get('force_platform_name','')
       if fpn!='':
          prop['name']=fpn

    if o=='con':
       ck.out('')
       ck.out('Platform name:   '+prop.get('name',''))
       ck.out('Platform vendor: '+prop.get('vendor',''))
       ck.out('Platform model:  '+prop.get('model',''))

    # Exchanging info #################################################################
    if ex=='yes':
       if o=='con':
          ck.out('')
          ck.out('Exchanging information with repository ...')

       xn=prop.get('name','')
       if xn=='':
          if o=='con':
             r=ck.inp({'text':'Enter your platform name (for example Samsung Chromebook 2, Huawei Ascend Mate 7, IBM SyNAPSE): '})
             xn=r['string']
          if xn=='':
             return {'return':1, 'error':'can\'t exchange information where main name is empty'}
          prop['name']=xn

       er=i.get('exchange_repo','')
       esr=i.get('exchange_subrepo','')
       if er=='': 
          er=ck.cfg['default_exchange_repo_uoa']
          esr=ck.cfg['default_exchange_subrepo_uoa']

       ii={'action':'exchange',
           'module_uoa':work['self_module_uid'],
           'sub_module_uoa':work['self_module_uid'],
           'repo_uoa':er,
           'data_name':prop.get('name',''),
           'all':'yes',
           'dict':{'features':prop}} # Later we should add more properties from prop_all,
                                     # but should be careful to remove any user-specific info
       if esr!='': ii['remote_repo_uoa']=esr
       r=ck.access(ii)
       if r['return']>0: return r

       prop=r['dict']

       if o=='con' and r.get('found','')=='yes':
          ck.out('  Data already exists - reloading ...')

    if 'features' not in rr: rr['features']={}

    rr['features']['platform']=prop
    rr['features']['platform_misc']=prop_all

    return rr

##############################################################################
# Get info from WMIC on Windows

def get_from_wmic(i):
    """
    Input:  {
              cmd     - cmd for wmic
              (group) - get the whole group
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              value        - obtained value
              (dict)       - if group
            }

    """

    import os

    value=''
    dd={}

    rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
    if rx['return']>0: return rx
    fn=rx['file_name']

    xcmd=i.get('cmd','')
    xgroup=i.get('group','')
    if xgroup!='': xcmd=xgroup

    cmd='wmic '+xcmd+' > '+fn
    r=os.system(cmd)
    if r!=0:
       return {'return':1, 'error':'command returned non-zero value: '+cmd}

    # Read and parse file
    rx=ck.load_text_file({'text_file':fn, 'encoding':'utf16', 'split_to_list':'yes'})
    if rx['return']>0: return rx
    ll=rx['lst']

    if os.path.isfile(fn): os.remove(fn)

    if xgroup=='':
       if len(ll)>1:
          value=ll[1].strip()
    else:
       if len(ll)>1:
          kk=ll[0]
          value=ll[1]

          xkeys=kk.split(' ')
          keys=[]
          for q in xkeys:
              if q!='': keys.append(q)

          for q in range(0, len(keys)):
              k=keys[q]

              if q==0: qx=0
              else: 
                 y=' '
                 if q==len(keys)-1: y=''
                 qx=kk.find(' '+k+y)

              if q==len(keys)-1:
                 qe=len(value)
              else:
                 qe=kk.find(' '+keys[q+1]+' ')

              v=value[qx:qe].strip()
              dd[k]=v

    return {'return':0, 'value':value, 'dict':dd}

##############################################################################
# Init remote device

def init_device(i):
    """
    Input:  {
              os_dict      - OS dict to get info about how to init device
              device_id    - ID of the device if more than one
              (key)        - key from OS to use, by default remote_init
                             useful for deinitialization, i.e. use key=remote_deinit
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    o=i.get('out','')

    key=i.get('key','')
    if key=='': key='remote_init'

    osd=i['os_dict']
    tdid=i['device_id'].strip()

    ri=osd.get(key,'')
    if ri!='':
       dv=''
       if tdid!='': dv=' -s '+tdid
       ri=ri.replace('$#device#$',dv)

       if o=='con':
          ck.out('Initializing remote device:')
          ck.out('')
          ck.out('  '+ri)

       rx=os.system(ri)
       if rx!=0:
          if o=='con':
             ck.out('')
             ck.out('Non-zero return code :'+str(rx)+' - likely failed')
          return {'return':1, 'error':'remote device initialization failed'}

       device_init='yes'

    return {'return':0}

##############################################################################
# exchange properties

def exchange(i):
    """
    Input:  {
              sub_module_uoa - module to search/exchange
              data_name      - data name to search

              (repo_uoa)     - where to record

              (dict)         - dictionary to check/record

              (all)          - if 'yes', check all dict['prop'] and add to separate file 

            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              dict         - if exists, load updated dict (can be collaboratively extended to add more properties!)
              (found)      - if 'yes', entry was found
            }

    """

    ruoa=i.get('repo_uoa','')
    smuoa=i['sub_module_uoa']

    dname=i.get('data_name','')

    dd=i.get('dict',{})
    ddf=dd.get('features',{})

    al=i.get('all','')

    if dname!='':
       # Search if already exists
       rx=ck.access({'action':'search',
                     'module_uoa':smuoa,
                     'repo_uoa':ruoa,
                     'search_by_name':dname,
                     'ignore_case':'yes'})
       if rx['return']>0: return rx
       lst=rx['lst']

       if len(lst)==0:
          # Add info
          rx=ck.access({'action':'add',
                        'module_uoa':smuoa,
                        'repo_uoa':ruoa,
                        'data_name':dname,
                        'dict':dd,
                        'sort_keys':'yes'})

       else:
          # Load
          ll=lst[0]
          duoa=ll.get('data_uid','')
          rx=ck.access({'action':'load',
                        'module_uoa':smuoa,
                        'repo_uoa':ruoa,
                        'data_uoa':duoa})

          rx['found']='yes'

       if rx['return']>0: return rx

       if al=='yes':
          # Check if extra parameters are saved
          import os
          p=rx['path']
          p1=os.path.join(p, 'all.json')

          dall={'all':[]}
          toadd=True

          if os.path.isfile(p1):
             ry=ck.load_json_file({'json_file':p1})
             if ry['return']>0: return ry
             dall=ry['dict']


             for q in dall.get('all',[]):
                 rz=ck.compare_dicts({'dict1':q, 'dict2':ddf})
                 if rz['return']>0: return rz
                 if rz['equal']=='yes':
                    toadd=False
                    break

          if toadd:
             dall['all'].append(ddf)

             rz=ck.save_json_to_file({'json_file':p1, 'dict':dall})
             if rz['return']>0: return rz

       return rx

    return {'return':1, 'error':'name is empty in platform information exchange'}

##############################################################################
# deinitialize device (put to powersave mode)

def deinit(i):
    """
    Input:  {
              (host_os)              - host OS (detect, if omitted)
              (os) or (target_os)    - OS module to check (if omitted, analyze host)
              (device_id)            - device id if remote (such as adb)
              (key)                  - {'remote_init' or 'remote_deinit'}
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    o=i.get('out','')

    # Various params
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    if tos=='': tos=i.get('os','')
    tdid=i.get('device_id','')

    # Get OS info
    import copy
    ii=copy.deepcopy(i)
    ii['out']=o
    ii['action']='detect'
    ii['skip_device_init']='yes'     # consider that device was already initialized
    ii['skip_info_collection']='yes'
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

    key=i.get('key','')
    if key=='': key='remote_deinit'

    ii={'os_dict':tosd,
        'device_id':tdid,
        'key':key,
        'out':o}
    return init_device(ii)
