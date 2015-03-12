#
# Collective Knowledge (platform - CPU)
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
# detect CPU

def detect(i):
    """
    Input:  {
              (os)        - OS module (needed to setup tools for CPU, if omitted use host)
              (device_id) - device id if remote (such as adb)
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

    xos=i.get('os','')
    device_id=i.get('device_id','')

    # Get info about host/target OS
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.os'],
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

    host_name=rr['host']['name']

    os_uoa=rr['os_uoa']
    os_uid=rr['os_uid']
    os_dict=rr['os_dict']

    remote=os_dict.get('remote','')
    os_win=os_dict.get('windows_base','')

    target={}
    info_cpu={}

    target_freq={}
    target_freq_max={}

    ro=os_dict.get('redirect_stdout','')

    if remote=='yes' or os_win!='yes':
       # Read cpuinfo
       fnx='/proc/cpuinfo'

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
          fcpuinfo=rx['file_name']

          x=os_dict.get('remote_shell','')+' cat '+fnx+' '+ro+fcpuinfo

          if o=='con':
             ck.out('')
             ck.out('Receiving info: '+x)

          rx=os.system(x)
          if rx!=0:
             if o=='con':
                ck.out('')
                ck.out('Non-zero return code :'+str(rx)+' - likely failed')
             return {'return':1, 'error':'access to remote device failed'}
       else:
          fcpuinfo=fnx

       # Read and parse file
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

       # Collect all frequencies
       for px in range(0, pp+1):
           fnx='/sys/devices/system/cpu/cpu'+str(px)+'/cpufreq/scaling_cur_freq'
           if remote=='yes':
              rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
              if rx['return']>0: return rx
              ffreq=rx['file_name']

              x=os_dict.get('remote_shell','')+' cat '+fnx+' '+ro+ffreq

              if o=='con':
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
           if rx['return']>0: return rx
           ll=rx['lst']
           if remote=='yes' and os.path.isfile(ffreq): os.remove(ffreq)

           if len(ll)>0:
              llx=ll[0].strip()
              if llx!='':
                 fr=float(llx)/1000
                 target_freq[str(px)]=fr

           fnx='/sys/devices/system/cpu/cpu'+str(px)+'/cpufreq/cpuinfo_max_freq'
           if remote=='yes':
              rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
              if rx['return']>0: return rx
              ffreq=rx['file_name']

              x=os_dict.get('remote_shell','')+' cat '+fnx+' '+ro+ffreq

              if o=='con':
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
           if rx['return']>0: return rx
           ll=rx['lst']
           if remote=='yes' and os.path.isfile(ffreq): os.remove(ffreq)

           if len(ll)>0:
              llx=ll[0].strip()
              if llx!='':
                 fr=float(llx)/1000
                 target_freq_max[str(px)]=fr

       target['name']=target_cpu
       target['num_proc']=target_num_proc
       target['current_freq']=target_freq
       target['max_freq']=target_freq_max








    else:
       if os_win=='yes':
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
          target['num_proc']=target_num_proc
          target['current_freq']={"0":target_freq}
          target['max_freq']={"0":target_freq_max}


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

    rr['cpu_properties_unified']=target
    rr['cpu_properties_all']=info_cpu

    return rr
