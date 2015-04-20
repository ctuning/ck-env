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
              (host_os)              - host OS (detect, if omitted)
              (os) or (target_os)    - OS module to check (if omitted, analyze host)

              (device_id)            - device id if remote (such as adb)
              (skip_device_init)     - if 'yes', do not initialize device
              (print_device_info)    - if 'yes', print extra device info

              (skip_info_collection) - if 'yes', do not collect info (particularly for remote)

              (exchange)             - if 'yes', exchange info with some repo (by default, remote-ck)
              (exchange_repo)        - which repo to record/update info (remote-ck by default)
              (exchange_subrepo)     - if remote, remote repo UOA

              (return_multi_devices) - if 'yes' and multiple devices detected, return error=32 and devices
            }

    Output: {
              return                - return code =  0, if successful
                                                  >  0, if error
              (error)               - error text if return > 0

              host_os_uoa            - host OS UOA
              host_os_uid            - host OS UID
              host_os_dict           - host OS meta

              os_uoa                 - target OS UOA
              os_uid                 - target OS UID
              os_dict                - target OS meta

              features = {
                os                   - OS features (properties), unified
                os_misc              - assorted OS features (properties), platform dependent
              }

              (devices)              - return devices if device_id==''
              (device_id)            - if device_id=='' and only 1 device, select it
            }

    """

    import os

    o=i.get('out','')

    # Various params
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    if tos=='': tos=i.get('os','')
    tdid=i.get('device_id','')

    sic=i.get('skip_info_collection','')
    sdi=i.get('skip_device_init','')
    pdv=i.get('print_device_info','')
    ex=i.get('exchange','')

    # Detect and find most close host OS or load already existing one
    r=ck.access({'action':'find_close',
                 'module_uoa':cfg['module_deps']['os'],
                 'os_uoa':hos})
    if r['return']>0: return r

    hos=r['os_uid']
    hosx=r['os_uoa']
    hosd=r['os_dict']

    # Checking/detecting host OS
    r=ck.access({'action':'find_close',
                 'module_uoa':cfg['module_deps']['os'],
                 'os_uoa':tos})
    if r['return']>0: return r

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    tp=r['platform']
    tbits=tosd.get('bits','')

    # Init params
    prop={}
    prop_all={}
    devices=[]

    prop_os_name=''
    prop_os_name_long=''
    prop_os_name_short=''

    ro=hosd.get('redirect_stdout','')

    remote=tosd.get('remote','')
    win=tosd.get('windows_base','')

    # Check devices, if remote
    if sic!='yes' and remote=='yes' and tdid=='':
       # Get devices
       rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
       if rx['return']>0: return rx
       fn=rx['file_name']

       x=tosd.get('adb_devices','')
       x=x.replace('$#redirect_stdout#$', ro)
       x=x.replace('$#output_file#$', fn)

       if o=='con' and pdv=='yes':
          ck.out('')
          ck.out('Receiving list of devices:')
          ck.out('  '+x)

       rx=os.system(x)
       if rx!=0:
          return {'return':1, 'error':'access to remote device failed (return code='+str(rx)+')'}

       # Read and parse file
       rx=ck.load_text_file({'text_file':fn, 
                             'split_to_list':'yes',
                             'delete_after_read':'yes'})
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

       if len(devices)==0:
          return {'return':1, 'error':'no attached remoted devices found'}

       if o=='con':
          ck.out('')
          ck.out('Available remote devices:')
          for q in devices:
              ck.out('  '+q)
          ck.out('')

       if tdid=='':
          if len(devices)==1:
             tdid=devices[0]
          else:
             if o=='con' and i.get('return_multi_devices','')!='yes':
                ck.out('')
                zz={}
                iz=0
                for j in range(0, len(devices)):
                    zs=str(j)
                    ck.out(zs+') '+devices[j])

                ck.out('')
                rx=ck.inp({'text':'Choose first number to select device: '})
                x=int(rx['string'].strip())

                if x<0 or x>=len(devices):
                   return {'return':1, 'error':'devic number is not recognized'}

                tdid=devices[x]
             else:
                return {'return':32, 'error':'more than one remote device - specify via device_id', 'devices':devices}

    # Collect additional info unless skipped
    if sic!='yes':
       if remote=='yes':
          # Initialized device if needed
          if sdi!='yes':
             remote_init=tosd.get('remote_init','')
             if remote_init!='':
                r=ck.access({'action':'init_device',
                             'module_uoa':cfg['module_deps']['platform'],
                             'os_dict':tosd,
                             'device_id':tdid})
                if r['return']>0: return r

          # Get all params
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

          prop_os_name='Android '+params.get('ro.build.version.release','')

          # Get proc version
          # Reuse fn as tmp name

          x=tosd['remote_shell']+' cat /proc/version '+tosd.get('remote_shell_end','')+' '+ro+' '+fn
          x=x.replace('$#device#$',dv)

          if o=='con' and pdv=='yes':
             ck.out('')
             ck.out('Receiving /proc/version:')
             ck.out('  '+x)

          rx=os.system(x)
          if rx==0:
             # Read and parse file
             rx=ck.load_text_file({'text_file':fn, 'split_to_list':'yes', 'delete_after_read':'yes'})
             if rx['return']>0: return rx
             ll=rx['lst']

             if len(ll)>0:
                prop_os_name_long=ll[0]
                prop_os_name_short=prop_os_name_long

                ix=prop_os_name_long.find(' (')
                if ix>=0:
                   ix1=prop_os_name_long.find('-')
                   if ix1>=0 and ix1<ix: ix=ix1
                   prop_os_name_short=prop_os_name_long[:ix]

       else:
          import platform
          prop_os_name_long=platform.platform()
          prop_os_name_short=platform.system()+' '+platform.release()

          if win=='yes':
             prop_os_name=prop_os_name_short
          else:
             # If Linux, remove extensions after - in a shorter version
             x=prop_os_name_short.find('-')
             if x>=0:
                prop_os_name_short=prop_os_name_short[:x]

             if prop_os_name=='':
                #Try to detect via /etc/*-release

                r=ck.gen_tmp_file({})
                if r['return']>0: return r
                fn=r['file_name']

                cmd='cat /etc/*-release > '+fn
                rx=os.system(cmd)
                if rx==0:
                   r=ck.load_text_file({'text_file':fn, 
                                        'convert_to_dict':'yes',
                                        'str_split':'=',
                                        'remove_quotes':'yes',
                                        'delete_after_read':'yes'})
                   if r['return']==0:
                      ver=r['dict']
                      prop_os_name=ver.get('DISTRIB_DESCRIPTION','')


    prop['ck_os_uoa']=tosx
    prop['ck_os_base_uoa']=tosd.get('base_uoa','')
    prop['name']=prop_os_name
    prop['name_long']=prop_os_name_long
    prop['name_short']=prop_os_name_short
    prop['bits']=tbits

    if o=='con':
       ck.out('')
       ck.out('OS CK UOA:     '+tosx+' ('+tos+')')
       ck.out('')
       ck.out('OS name:       '+prop.get('name',''))
       ck.out('Short OS name: '+prop.get('name_short',''))
       ck.out('Long OS name:  '+prop.get('name_long',''))
       ck.out('OS bits:       '+prop.get('bits',''))

    # Exchanging info #################################################################
    if ex=='yes':
       if o=='con':
          ck.out('')
          ck.out('Exchanging information with repository ...')

       xn=prop.get('name','')
       if xn=='':
          if o=='con':
             r=ck.inp({'text':'Enter your OS name (for example, Windows 10 or Android 5.0): '})
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
           'module_uoa':cfg['module_deps']['platform'],
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

    return {'return':0, 'os_uoa':tosx, 'os_uid':tos, 'os_dict':tosd, 
                        'host_os_uoa':hosx, 'host_os_uid':hos, 'host_os_dict':hosd,
                        'features':{'os':prop, 'os_misc':prop_all}, 
                        'devices':devices, 'device_id':tdid}
