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
              (os)        - OS module to check (if omitted, analyze host)
              (device_id) - device id if remote and adb
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              os_ck
              os
            }

    """

    import os

    o=i.get('out','')

    oo=''
    if o=='con': oo=o

    xos=i.get('os','')
    device_id=i.get('device_id','')

    target={}

    # Get info about host/target OS and CPU at the same time
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.cpu'],
        'os':xos,
        'device_id':device_id}
    rr=ck.access(ii)
    if rr['return']>0: return rr # Careful will be updating this rr

    prop=rr['os_properties_unified']
    os_uoa=rr['os_uoa']
    os_uid=rr['os_uid']

    if o=='con':
       ck.out('')
       ck.out('OS CK UOA:     '+os_uoa+' ('+os_uid+')')
       ck.out('')
       ck.out('Short OS name: '+prop.get('name_short',''))
       ck.out('Long OS name:  '+prop.get('name_long',''))
       ck.out('OS bits:       '+prop.get('bits',''))

    target=rr['cpu_properties_unified']

    if o=='con':
       ck.out('')
       ck.out('Number of logical processors: '+str(target.get('num_proc',0)))
       ck.out('')
       ck.out('CPU name:                     '+target.get('name',''))
       ck.out('')
       ck.out('CPU frequency:')
       x=target.get('current_freq',{})
       for k in sorted(x, key=ck.convert_str_key_to_int):
           v=x[k]
           ck.out('  CPU'+k+' = '+str(v)+' MHz')
       ck.out('CPU max frequency:')
       x=target.get('max_freq',{})
       for k in sorted(x, key=ck.convert_str_key_to_int):
           v=x[k]
           ck.out('  CPU'+k+' = '+str(v)+' MHz')

    xos=rr['os_uoa']
    device_id=rr['device_id']

    host_name=rr['host']['name']

    os_uoa=rr['os_uoa']
    os_uid=rr['os_uid']
    os_dict=rr['os_dict']

    remote=os_dict.get('remote','')
    os_win=os_dict.get('windows_base','')

    ro=os_dict.get('redirect_stdout','')

    # Get info about accelerator (GPU)
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.accelerator'],
        'os':xos,
        'device_id':device_id}
    rx=ck.access(ii)
    if rx['return']>0: return rx # Careful will be updating this rr

    gpu=rx['gpu_properties_unified']

    ck.out('')
    ck.out('GPU name: '+gpu.get('name',''))

    rr.update(rx)

    info1={}

    # Get info about system ######################################################
    remote=os_dict.get('remote','')
    if remote=='yes':
       remote_init=os_dict.get('remote_init','')
       if remote_init!='':
#          if o=='con':
#             ck.out('Initializing remote device:')
#             ck.out('  '+remote_init)
#             ck.out('')

          rx=os.system(remote_init)
          if rx!=0:
#             if o=='con':
#                ck.out('')
#                ck.out('Non-zero return code :'+str(rx)+' - likely failed')
             return {'return':1, 'error':'remote device initialization failed'}

       # Get devices
       rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
       if rx['return']>0: return rx
       fn=rx['file_name']

       adb_devices=os_dict.get('adb_devices','')
       adb_devices=adb_devices.replace('$#redirect_stdout#$', ro)
       adb_devices=adb_devices.replace('$#output_file#$', fn)

#       if o=='con':
#          ck.out('')
#          ck.out('Receiving list of devices:')
#          ck.out('  '+adb_devices)

       rx=os.system(adb_devices)
       if rx!=0:
#          if o=='con':
#             ck.out('')
#             ck.out('Non-zero return code :'+str(rx)+' - likely failed')
          return {'return':1, 'error':'access to remote device failed'}

       # Read and parse file
       rx=ck.load_text_file({'text_file':fn, 'split_to_list':'yes'})
       if rx['return']>0: return rx
       ll=rx['lst']

       devices=[]
       for q in range(1, len(ll)):
           s1=ll[q].strip()
           if s1!='':
              q2=s1.find('\t')
              if q2>0:
                 s2=s1[0:q2]
                 devices.append(s2)

       if os.path.isfile(fn): os.remove(fn)

       if o=='con':
          ck.out('')
          ck.out('Available remote devices:')
          for q in devices:
              ck.out('  '+q)
          ck.out('')

       if device_id!='':
          if device_id not in devices:
             return {'return':1, 'error':'Device ID was not found in the list of attached devices'}
       else:
          if len(devices)>0:
             device_id=devices[0]

       # Get all params
       params={}

       rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
       if rx['return']>0: return rx
       fn=rx['file_name']

       adb_params=os_dict.get('adb_all_params','')
       adb_params=adb_params.replace('$#redirect_stdout#$', ro)
       adb_params=adb_params.replace('$#output_file#$', fn)

#       if o=='con':
#          ck.out('')
#          ck.out('Receiving all parameters:')
#          ck.out('  '+adb_params)

       rx=os.system(adb_params)
       if rx!=0:
#          if o=='con':
#             ck.out('')
#             ck.out('Non-zero return code :'+str(rx)+' - likely failed')
          return {'return':1, 'error':'access to remote device failed'}

       # Read and parse file
       rx=ck.load_text_file({'text_file':fn, 'split_to_list':'yes'})
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

       if os.path.isfile(fn): os.remove(fn)

#       for q in params:
#           v=params[q]
#           print q+'='+v

       target['system_name']=params.get('ro.product.model','')
       target['model']=params.get('ro.product.board','')
    else:
       if os_win=='yes':
          r=get_from_wmic({'group':'csproduct'})
          if r['return']>0: return r
          info1=r['dict']

          x1=info1.get('Vendor','')
          x2=info1.get('Version','')

          target_system_name=x1+' '+x2

          r=get_from_wmic({'cmd':'computersystem get model'})
          if r['return']>0: return r
          target_system_model=r['value']

          target['system_name']=target_system_name
          target['model']=target_system_model
       else:
          x1=''
          x2=''
          info1={}

          target_system_model=''
          target_system_name=''

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
             target_system_name=x1+' '+x2

          file_with_id='/sys/devices/virtual/dmi/id/product_name'
          if os.path.isfile(file_with_id):
             r=ck.load_text_file({'text_file':file_with_id})
             if r['return']>0: return r
             target_system_model=r['string'].strip()

          target['system_name']=target_system_name
          target['model']=target_system_model

    if o=='con':
       ck.out('')
       ck.out('System name:        '+target.get('system_name',''))
       ck.out('System model:       '+target.get('model',''))

    rr['cpu_properties_unified']=target
    rr['cpu_properties_all']={'cs_product':info1}

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
