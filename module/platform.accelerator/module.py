#
# Collective Knowledge (platform - accelerator)
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
# Detect accelerators (GPU, etc)

def detect(i):
    """
    Input:  {
              (os)               - OS module (needed to setup tools for CPU, if omitted use host)
              (device_id)        - device id if remote (such as adb)

              (exchange)         - if 'yes', exchange info with some repo (by default, remote-ck)
              (exchange_repo)    - which repo to record/update info (remote-ck by default)
              (exchange_subrepo) - if remote, remote repo UOA
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    o=i.get('out','')

    xos=i.get('os','')
    device_id=i.get('device_id','')

    # Get info about host/target OS
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.os'],
        'os':xos,
        'device_id':device_id}
    rr=ck.access(ii)
    if rr['return']>0: return rr # Careful will be updating this rr

    host_name=rr['host']['name']

    os_uoa=rr['os_uoa']
    os_uid=rr['os_uid']
    os_dict=rr['os_dict']

    remote=os_dict.get('remote','')
    os_win=os_dict.get('windows_base','')

    target={}

    ro=os_dict.get('redirect_stdout','')

    # Get info about accelerator ######################################################
    remote=os_dict.get('remote','')
    if remote=='yes':
       remote_init=os_dict.get('remote_init','')
       if remote_init!='':
          if o=='con':
             ck.out('Initializing remote device:')
             ck.out('  '+remote_init)
             ck.out('')

          rx=os.system(remote_init)
          if rx!=0:
             if o=='con':
                ck.out('')
                ck.out('Non-zero return code :'+str(rx)+' - likely failed')
             return {'return':1, 'error':'remote device initialization failed'}

       # Get devices
       rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
       if rx['return']>0: return rx
       fn=rx['file_name']

       adb_devices=os_dict.get('adb_devices','')
       adb_devices=adb_devices.replace('$#redirect_stdout#$', ro)
       adb_devices=adb_devices.replace('$#output_file#$', fn)

       if o=='con':
          ck.out('')
          ck.out('Receiving list of devices:')
          ck.out('  '+adb_devices)

       rx=os.system(adb_devices)
       if rx!=0:
          if o=='con':
             ck.out('')
             ck.out('Non-zero return code :'+str(rx)+' - likely failed')
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

       # Get GPU
       adb_params=os_dict.get('adb_dumpsys','')
       adb_params=adb_params.replace('$#category#$','SurfaceFlinger')
       adb_params=adb_params.replace('$#redirect_stdout#$', ro)
       adb_params=adb_params.replace('$#output_file#$', fn)

       if o=='con':
          ck.out('')
          ck.out('Receiving all parameters:')
          ck.out('  '+adb_params)

       rx=os.system(adb_params)
       if rx!=0:
          if o=='con':
             ck.out('')
             ck.out('Non-zero return code :'+str(rx)+' - likely failed')
          return {'return':1, 'error':'access to remote device failed'}

       # Read and parse file
       rx=ck.load_text_file({'text_file':fn, 'split_to_list':'yes'})
       if rx['return']>0: return rx
       ll=rx['lst']

       for s in ll:
           s1=s.strip()
           q2=s1.find('GLES: ')
           if q2>=0:
              target_gpu_name=s1[6:].strip()

              target['name']=target_gpu_name
              target['possibly_related_cpu_name']=''

              break
       if os.path.isfile(fn): os.remove(fn)
    else:
       if os_win=='yes':
          r=ck.access({'action':'get_from_wmic',
                       'module_uoa':cfg['module_deps']['platform'],
                       'group':'cpu'})
          if r['return']>0: return r
          info_cpu=r['dict']

          target_cpu=info_cpu.get('Name','')

          r=ck.access({'action':'get_from_wmic',
                       'module_uoa':cfg['module_deps']['platform'],
                       'cmd':'path Win32_VideoController get Name'})
          if r['return']>0: return r
          target_gpu_name=r['value']

          target['name']=target_gpu_name
          target['possibly_related_cpu_name']=target_cpu

       else:
          # Get devices
          rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
          if rx['return']>0: return rx
          fn=rx['file_name']

          x='lspci '+ro+' '+fn

          if o=='con':
             ck.out('')
             ck.out('Executing: '+x)

          rx=os.system(x)
          if rx!=0:
             if o=='con':
                ck.out('')
                ck.out('Non-zero return code :'+str(rx)+' - likely failed')
             return {'return':1, 'error':'executing lspci likely failed'}

          # Read and parse file
          rx=ck.load_text_file({'text_file':fn, 'split_to_list':'yes'})
          if rx['return']>0: return rx
          ll=rx['lst']

          for q in ll:
              x1=q.find('VGA ')
              if x1>=0:
                 x2=q.find(':', x1+1)
                 if x2>=0:
                    target_gpu_name=q[x2+1:].strip()
                    break

          if os.path.isfile(fn): os.remove(fn)

          target['name']=target_gpu_name

    if o=='con':
       ck.out('')
       ck.out('GPU name: '+target.get('name',''))

    rr['gpu_properties_unified']=target

    return rr
