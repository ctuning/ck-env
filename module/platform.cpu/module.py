#
# Collective Knowledge (platform - CPU)
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
# detect CPU

def detect(i):
    """
    Input:  {
              (host_os)              - host OS (detect, if omitted)
              (os) or (target_os)    - OS module to check (if omitted, analyze host)

              (device_id)            - device id if remote (such as adb)
              (skip_device_init)     - if 'yes', do not initialize device
              (print_device_info)    - if 'yes', print extra device info

              (skip_info_collection) - if 'yes', do not collect info (particularly for remote)

              (skip_print_os_info)   - if 'yes', do not print OS info

              (exchange)             - if 'yes', exchange info with some repo (by default, remote-ck)
              (share)                - the same as 'exchange'
              (exchange_repo)        - which repo to record/update info (remote-ck by default)
              (exchange_subrepo)     - if remote, remote repo UOA
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              features = {
                cpu        - CPU features (properties), unified
                cpu_misc   - assorted CPU features (properties), platform dependent

                os         - OS features (properties), unified
                os_misc    - assorted OS features (properties), platform dependent
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

    # Get OS info ##############################################################
    import copy
    ii=copy.deepcopy(i)
    ii['out']=oo
    if i.get('skip_print_os_info','')=='yes':ii['out']=''
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

    # Some params
    ro=tosd.get('redirect_stdout','')
    remote=tosd.get('remote','')
    win=tosd.get('windows_base','')

    dv=''
    if tdid!='': dv=' -s '+tdid

    # Init
    target={}
    target_freq={}
    target_freq_all={}
    target_freq_max={}
    target_num_proc=''
    info_cpu={}

    if remote=='yes' or win!='yes':
       # Read cpuinfo
       fnx='/proc/cpuinfo'

       if remote=='yes':

          # Read file
          rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
          if rx['return']>0: return rx
          fcpuinfo=rx['file_name']

          x=tosd.get('remote_shell','').replace('$#device#$',dv)+' cat '+fnx+' '+tosd.get('remote_shell_end','')+' '+ro+fcpuinfo

          if o=='con' and pdv=='yes':
             ck.out('')
             ck.out('Receiving info: '+x)

          rx=os.system(x)
          if rx!=0: 
             if os.path.isfile(fnx): os.remove(fcpuinfo)
             fcpuinfo='' # Do not process further

       else:
          fcpuinfo=fnx

       # Read and parse file
       if fcpuinfo!='':
          rx=ck.load_text_file({'text_file':fcpuinfo, 'split_to_list':'yes'})
          if rx['return']>0: return rx
          ll=rx['lst']
          if remote=='yes' and os.path.isfile(fcpuinfo): os.remove(fcpuinfo)

          pp=0 # current logical processor
          spp=str(pp)
          info_cpu[spp]={}
          target_freq[spp]=0
          target_freq_max[spp]=0
          first_skipped=False
          for q in ll:
              q=q.strip()
              if q!='':
                 x1=q.find(':')
                 if x1>0:
                    k=q[0:x1-1].strip()
                    v=q[x1+1:].strip()

                    if k=='processor':
                       if not first_skipped:
                          first_skipped=True
                       else:
                          pp+=1
                          spp=str(pp)
                          info_cpu[spp]={}

                    if k!='':
                       info_cpu[spp][k]=v

                       if k.find('MHz')>=0:
                          target_freq[spp]=float(v)
          target_num_proc=str(pp+1)

       target_cpu=info_cpu[spp].get('Hardware','')
       if target_cpu=='':
          target_cpu=info_cpu[spp].get('model name','')
       target_sub_cpu=info_cpu[spp].get('Processor','')
       if target_sub_cpu=='':
          target_sub_cpu=info_cpu[spp].get('model name','')
       target_cpu_features=info_cpu[spp].get('Features','')
       if target_cpu_features=='':
          target_cpu_features=info_cpu[spp].get('flags','')

       # Collect all frequencies
       for px in range(0, pp+1):
           fnx='/sys/devices/system/cpu/cpu'+str(px)+'/cpufreq/scaling_cur_freq'
           if remote=='yes':
              rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
              if rx['return']>0: return rx
              ffreq=rx['file_name']

              x=tosd.get('remote_shell','').replace('$#device#$',dv)+' cat '+fnx+' '+tosd.get('remote_shell_end','')+' '+ro+ffreq

              if o=='con' and pdv=='yes':
                 ck.out('')
                 ck.out('Receiving info: '+x)

              rx=os.system(x)
              if rx!=0:
                 if o=='con':
                    ck.out('')
                    ck.out('Non-zero return code :'+str(rx)+' - likely failed')
                 return {'return':1, 'error':'access to remote device failed'}
           else:
              ffreq=fnx

           # Read and parse file
           rx=ck.load_text_file({'text_file':ffreq, 'split_to_list':'yes'})
           if rx['return']==0: 
              ll=rx['lst']
              if remote=='yes' and os.path.isfile(ffreq): os.remove(ffreq)

              if len(ll)>0:
                 llx=ll[0].strip()
                 if llx!='':
                    fr=0
                    try:
                      fr=float(llx)/1000
                      target_freq[str(px)]=fr
                    except ValueError:
                      pass

           fnx='/sys/devices/system/cpu/cpu'+str(px)+'/cpufreq/cpuinfo_max_freq'
           if remote=='yes':
              rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
              if rx['return']>0: return rx
              ffreq=rx['file_name']

              x=tosd.get('remote_shell','').replace('$#device#$',dv)+' cat '+fnx+' '+tosd.get('remote_shell_end','')+' '+ro+ffreq

              if o=='con' and pdv=='yes':
                 ck.out('')
                 ck.out('Receiving info: '+x)

              rx=os.system(x)
              if rx!=0:
                 if o=='con':
                    ck.out('')
                    ck.out('Non-zero return code :'+str(rx)+' - likely failed')
                 return {'return':1, 'error':'access to remote device failed'}
           else:
              ffreq=fnx

           # Read and parse file
           rx=ck.load_text_file({'text_file':ffreq, 'split_to_list':'yes'})
           if rx['return']==0:
              ll=rx['lst']
              if remote=='yes' and os.path.isfile(ffreq): os.remove(ffreq)

              if len(ll)>0:
                 llx=ll[0].strip()
                 if llx!='':
                    try:
                      fr=float(llx)/1000
                      target_freq_max[str(px)]=fr
                    except ValueError:
                      pass

           fnx='/sys/devices/system/cpu/cpu'+str(px)+'/cpufreq/scaling_available_frequencies'
           if remote=='yes':
              rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
              if rx['return']>0: return rx
              ffreq=rx['file_name']

              x=tosd.get('remote_shell','').replace('$#device#$',dv)+' cat '+fnx+' '+tosd.get('remote_shell_end','')+' '+ro+ffreq

              if o=='con' and pdv=='yes':
                 ck.out('')
                 ck.out('Receiving info: '+x)

              rx=os.system(x)
              if rx!=0:
                 if o=='con':
                    ck.out('')
                    ck.out('Non-zero return code :'+str(rx)+' - likely failed')
                 return {'return':1, 'error':'access to remote device failed'}
           else:
              ffreq=fnx

           # Read and parse file
           rx=ck.load_text_file({'text_file':ffreq, 'split_to_list':'yes'})
           if rx['return']==0:
              ll=rx['lst']
              if remote=='yes' and os.path.isfile(ffreq): os.remove(ffreq)

              if len(ll)>0:
                 llx=ll[0].strip()
                 if llx!='':
                    all=llx.split(' ')
                    for h in all:
                        ppx=str(px)
                        if ppx not in target_freq_all: target_freq_all[ppx]=[]
                        try:
                           h=int(h)
                           target_freq_all[ppx].append(h)
                        except ValueError:
                           pass


# FGG - it is already initalized here!
#       # Initialized device if needed
#       if sdi!='yes':
#          remote_init=tosd.get('remote_init','')
#          if remote_init!='':
#             r=ck.access({'action':'init_device',
#                          'module_uoa':cfg['module_deps']['platform'],
#                          'os_dict':tosd,
#                          'device_id':tdid})
#             if r['return']>0: return r

       # Get all params
       params={}
       if remote=='yes':
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

       target['name']=target_cpu
       target['sub_name']=target_sub_cpu
       target['cpu_features']=target_cpu_features
       target['cpu_abi']=params.get('ro.product.cpu.abi','')
       target['num_proc']=target_num_proc
       target['current_freq']=target_freq
       target['max_freq']=target_freq_max
       target['all_freqs']=target_freq_all

    else:
       if win=='yes':
          r=ck.access({'action':'get_from_wmic',
                       'module_uoa':cfg['module_deps']['platform'],
                       'group':'cpu'})
          if r['return']>0: return r
          info_cpu=r['dict']

          target_cpu=info_cpu.get('Name','')

          target_freq=int(info_cpu.get('CurrentClockSpeed','0'))
          target_freq_max=int(info_cpu.get('MaxClockSpeed','0'))

          target_num_proc=int(info_cpu.get('NumberOfLogicalProcessors','0'))

          target['name']=target_cpu
          target['sub_name']=target_cpu
          target['num_proc']=target_num_proc
          target['current_freq']={"0":target_freq}
          target['max_freq']={"0":target_freq_max}

    if o=='con':
       ck.out('')
       ck.out('Number of logical processors: '+str(target.get('num_proc',0)))
       ck.out('CPU name:                     '+target.get('name',''))
       if target.get('name','')!=target.get('sub_name',''):
          ck.out('CPU sub name:                 '+target.get('sub_name',''))
       ck.out('CPU ABI:                      '+target.get('cpu_abi',''))
       ck.out('CPU features:                 '+target.get('cpu_features',''))
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

       x=target.get('all_freqs',{})
       if len(x)>0:
          ck.out('CPU all frequencies (Hz):')
          import json
          for k in sorted(x, key=ck.convert_str_key_to_int):
              v=x[k]
              ck.out('  CPU'+k+' = '+json.dumps(v))

    # Exchanging info #################################################################
    if ex=='yes':
       if o=='con':
          ck.out('')
          ck.out('Exchanging information with repository ...')

       xn=target.get('name','')
       if xn=='':
          if o=='con':
             r=ck.inp({'text':'Enter your processor name: '})
             xn=r['string']
          if xn=='':
             return {'return':1, 'error':'can\'t exchange information where main name is empty'}
          target['name']=xn

       er=i.get('exchange_repo','')
       esr=i.get('exchange_subrepo','')
       if er=='': 
          er=ck.cfg['default_exchange_repo_uoa']
          esr=ck.cfg['default_exchange_subrepo_uoa']

       ii={'action':'exchange',
           'module_uoa':cfg['module_deps']['platform'],
           'sub_module_uoa':work['self_module_uid'],
           'repo_uoa':er,
           'data_name':target.get('name',''),
           'all':'no',
           'dict':{'features':target}} # Later we should add more properties from prop_all,
                                       # but should be careful to remove any user-specific info
       if esr!='': ii['remote_repo_uoa']=esr
       r=ck.access(ii)
       if r['return']>0: return r

       prop=r['dict']

       if o=='con' and r.get('found','')=='yes':
          ck.out('  Data already exists - reloading ...')

    if 'features' not in rr: rr['features']={}

    rr['features']['cpu']=target
    rr['features']['cpu_misc']=info_cpu

    return rr

##############################################################################
# set frequency

def set_freq(i):
    """
    Input:  {
              (host_os)              - host OS (detect, if omitted)
              (os) or (target_os)    - OS module to check (if omitted, analyze host)

              (device_id)            - device id if remote (such as adb)

              (value) = "max" (default)
                        "min"
                        int value
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    o=i.get('out','')
    oo=''
    if o=='con': oo=o

    v=i.get('value','')
    if v=='': v='max'

    # Various params
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    if tos=='': tos=i.get('os','')
    tdid=i.get('device_id','')

    # Get OS info
    import copy
    ii=copy.deepcopy(i)
    ii['out']=''
    ii['action']='detect'
    ii['module_uoa']=cfg['module_deps']['platform.os']
    ii['skip_info_collection']='yes'
    ii['skip_device_init']='yes'
    rr=ck.access(ii)
    if rr['return']>0: return rr

    hos=rr['host_os_uid']
    hosx=rr['host_os_uoa']
    hosd=rr['host_os_dict']

    tos=rr['os_uid']
    tosx=rr['os_uoa']
    tosd=rr['os_dict']

    tbits=tosd.get('bits','')

    tdid=rr['device_id']

    dir_sep=tosd.get('dir_sep','')

    remote=tosd.get('remote','')

    # Prepare scripts
    cmd=''
    if v=='min':
       cmd=tosd.get('script_set_min_cpu_freq','')
    elif v=='max':
       cmd=tosd.get('script_set_max_cpu_freq','')
    else:
       cmd=tosd.get('script_set_cpu_freq','').replace('$#freq#$',str(v))

    if cmd!='':
       # Check path to scripts from env
       path_to_scripts=''
       piu=os.environ.get('CK_PLATFORM_INIT_UOA','')
       if piu!='' and remote!='yes':
          rx=ck.access({'action':'find',
                        'module_uoa':cfg['module_deps']['platform.init'],
                        'data_uoa':piu})
          if rx['return']>0: return rx
          path_to_scripts=rx['path']

       if path_to_scripts=='':
          path_to_scripts=tosd.get('path_to_scripts','')

       if path_to_scripts!='': cmd=path_to_scripts+dir_sep+cmd

       if o=='con':
          ck.out('')
          ck.out('CMD to set CPU frequency:')
          ck.out('  '+cmd)

       # Get all params
       if remote=='yes':
          dv=''
          if tdid!='': dv=' -s '+tdid

          x=tosd.get('remote_shell','').replace('$#device#$',dv)+' '+cmd

          rx=os.system(x)
          if rx!=0:
             if o=='con':
                ck.out('')
                ck.out('Non-zero return code :'+str(rx)+' - likely failed')

       else:
             rx=os.system(cmd)
             if rx!=0:
                if o=='con':
                   ck.out('')
                   ck.out('  Warning: setting frequency possibly failed - return code '+str(rx))

    return {'return':0}
