#
# Collective Knowledge (platform - OS)
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
# detect OS

def detect(i):
    """
    Input:  {
              (os)        - OS module to check (if omitted, analyze host)
              (device_id) - device id if remote (such as adb)

              (skip_info_collection) - if 'yes', do not collect info (particularly for remote)

              (exchange)         - if 'yes', exchange info with some repo (by default, remote-ck)
              (exchange_repo)    - which repo to record/update info (remote-ck by default)
              (exchange_subrepo) - if remote, remote repo UOA
            }

    Output: {
              return                - return code =  0, if successful
                                                  >  0, if error
              (error)               - error text if return > 0

              os_uoa
              os_uid
              os_cfg
              os_properties_unified
              os_properties_all
              device_id
            }

    """

    import os

    o=i.get('out','')

    ex=i.get('exchange','')

    sic=i.get('skip_info_collection','')

    host={}
    prop={}
    prop_all={}
    work={}

    xos=i.get('os','')

    # Get a few host parameters + target platform
    r=ck.get_os_ck({'os_uoa':xos, 'find_close':'yes'})
    if r['return']>0: return r

    host_name=r['platform']
    host_bits=r['bits']
    host_cfg=ck.cfg.get('shell',{}).get(host_name,{})

    host['name']=host_name
    host['bits']=host_bits
    host['cfg']=host_cfg

    ro=host_cfg.get('redirect_stdout','')

    # Retrieved (most close) platform
    os_uoa=r['os_uoa']
    os_uid=r['os_uid']

    os_dict=r['os_dict']

    prop['uoa']=os_uoa
    prop['uid']=os_uid
    prop['dict']=os_dict

    device_id=i.get('device_id','')

    # Checking platform
    os_bits=os_dict.get('bits','')
    os_win=os_dict.get('windows_base','')

    prop_os_name_long=''
    prop_os_name_short=''
    prop_os_name_sub=''   # On Android, name of Linux

    if sic!='yes':
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

          prop['devices']=devices

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

              q2=s1.find(']: [')
              k=''
              if q2>=0:
                 k=s1[1:q2].strip()
                 v=s1[q2+4:].strip()
                 v=v[:-1].strip()

                 params[k]=v

          prop['params']=params

          if os.path.isfile(fn): os.remove(fn)

          # Get params
          x1=params.get('ro.product.brand','')
          x2=params.get('ro.product.model','')

          prop_system_name=x1+' '+x2

          prop_system_model=x2

          prop_os_name_long=params.get('ro.build.kernel.version','')
          prop_os_name_short='Android '+params.get('ro.build.version.release','')
          





       else:
          import platform
          prop_os_name_long=platform.platform()
          prop_os_name_short=platform.system()+' '+platform.release()

    prop['name_long']=prop_os_name_long
    prop['name_short']=prop_os_name_short
    prop['bits']=os_bits

    if o=='con':
       ck.out('OS CK UOA:     '+os_uoa+' ('+os_uid+')')
       ck.out('')
       ck.out('Short OS name: '+prop_os_name_short)
       ck.out('Long OS name:  '+prop_os_name_long)
       ck.out('Sub OS name:   '+prop_os_name_sub)
       ck.out('OS bits:       '+os_bits)
       ck.out('')

    if ex=='yes':
       if o=='con':
          ck.out('Trying to exchange information with repository ...')

       er=i.get('exchange_repo','')
       esr=i.get('exchange_subrepo','')

       if er=='': 
          er=cfg['default_exchange_repo_uoa']
          if esr=='': esr=cfg['default_exchange_subrepo_uoa']













    return {'return':0, 'os_uoa':os_uoa, 'os_uid':os_uid, 'os_dict':os_dict, 
                        'host':host,
                        'properties_unified':prop, 'properties_all':prop_all, 
                        'device_id':device_id}
