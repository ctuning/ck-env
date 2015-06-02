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
              (host_os)              - host OS (detect, if omitted)
              (os) or (target_os)    - OS module to check (if omitted, analyze host)

              (device_id)            - device id if remote (such as adb)
              (skip_device_init)     - if 'yes', do not initialize device
              (print_device_info)    - if 'yes', print extra device info

              (skip_info_collection) - if 'yes', do not collect info (particularly for remote)

              (skip_print_os_info)   - if 'yes', do not print OS info

              (exchange)             - if 'yes', exchange info with some repo (by default, remote-ck)
              (exchange_repo)        - which repo to record/update info (remote-ck by default)
              (exchange_subrepo)     - if remote, remote repo UOA
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              features = {
                acc          - Accelerator features (properties), unified
                acc_misc     - assorted Accelerator features (properties), platform dependent
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

    # Get OS info
    import copy
    ii=copy.deepcopy(i)
    ii['out']=oo
    if i.get('skip_print_os_info','')=='yes': ii['out']=''
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

    stdirs=tosd.get('dir_sep','')

    dv=''
    if tdid!='': dv=' -s '+tdid

    # Init
    prop={}
    prop_all={}

    target_gpu_name=''

    # Get info about accelerator ######################################################
    if remote=='yes':
       # Get all params
       params={}

       rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
       if rx['return']>0: return rx
       fn=rx['file_name']

       # Get GPU
       x=tosd.get('adb_dumpsys','').replace('$#device#$',dv)
       x=x.replace('$#category#$','SurfaceFlinger')
       x=x.replace('$#redirect_stdout#$', ro)
       x=x.replace('$#output_file#$', fn)

       if o=='con' and pdv=='yes':
          ck.out('')
          ck.out('Receiving all parameters:')
          ck.out('  '+x)

       rx=os.system(x)
       if rx!=0:
          if o=='con':
             ck.out('')
             ck.out('Non-zero return code :'+str(rx)+' - likely failed')
       else:
          # Read and parse file
          rx=ck.load_text_file({'text_file':fn, 'split_to_list':'yes', 'delete_after_read':'yes'})
          if rx['return']>0: return rx
          ll=rx['lst']

          for s in ll:
              s1=s.strip()
              q2=s1.find('GLES: ')
              if q2>=0:
                 target_gpu_name=s1[6:].strip()

                 prop['name']=target_gpu_name
                 prop['possibly_related_cpu_name']=''

                 break
    else:
       if win=='yes':
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

          prop['name']=target_gpu_name
          prop['possibly_related_cpu_name']=target_cpu

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
          if rx==0:
             # Read and parse file
             rx=ck.load_text_file({'text_file':fn, 'split_to_list':'yes', 'delete_after_read':'yes'})
             if rx['return']==0: 
                ll=rx['lst']

                for q in ll:
                    x1=q.find('VGA ')
                    if x1>=0:
                       x2=q.find(':', x1+1)
                       if x2>=0:
                          target_gpu_name=q[x2+1:].strip()
                          break

          prop['name']=target_gpu_name

    if o=='con' and prop.get('name','')!='':
       ck.out('')
       ck.out('GPU name: '+prop.get('name',''))

    # Check frequency via script
    if win!='yes':
       rx=ck.gen_tmp_file({'prefix':'tmp-ck-'})
       if rx['return']>0: return rx
       fn=rx['file_name']

       cmd=tosd.get('script_get_gpu_frequency','')+' '+ro+fn

       path_to_scripts=tosd.get('path_to_scripts','')
       if path_to_scripts!='': cmd=path_to_scripts+stdirs+cmd

       if remote=='yes':
          # Execute script
          cmd=tosd.get('remote_shell','').replace('$#device#$',dv)+' '+cmd

       if o=='con':
          ck.out('')
          ck.out('Trying to read GPU frequency:')
          ck.out('  '+cmd)

       rx=os.system(cmd)
       if rx!=0:
          if o=='con':
             ck.out('')
             ck.out('Non-zero return code :'+str(rx)+' - likely failed')
             ck.out('')
       else:
          # Read and parse file
          rx=ck.load_text_file({'text_file':fn, 'split_to_list':'yes', 'delete_after_read':'yes'})
          if rx['return']>0: return rx
          ll=rx['lst']

          cur_freq=''
          freqs=[]

          jl=len(ll)
          for j in range(0,jl):
              s=ll[j]
              if s.lower().startswith('*** current gpu frequency:'):
                 if (j+1)<jl:
                    cur_freq=ll[j+1]

              if s.lower().startswith('*** available gpu frequencies:'):
                 while s!='' and j<jl:
                    j+=1
                    if j<jl:
                       s=ll[j]
                       if s!='':
                          freqs.append(s)
                 break

          prop['current_freq']=cur_freq
          prop['all_freqs']=freqs

          if o=='con' and cur_freq!='':
             ck.out('')
             ck.out('Current GPU frequency:')
             ck.out('  '+str(cur_freq))
             if len(freqs)>0:
                ck.out('')
                ck.out('All frequencies:')
                for q in freqs:
                    ck.out(' '+q)

    # Exchanging info #################################################################
    if ex=='yes':
       if o=='con':
          ck.out('')
          ck.out('Exchanging information with repository ...')

       xn=prop.get('name','')
       if xn=='':
          if o=='con':
             r=ck.inp({'text':'Enter your accelerator name (for example ARM MALI-T860, Nvidia Tesla K80): '})
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

    if 'features' not in rr: rr['features']={}

    rr['features']['acc']=prop
    rr['features']['acc_misc']=prop_all

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
       cmd=tosd.get('script_set_min_gpu_freq','')
    elif v=='max':
       cmd=tosd.get('script_set_max_gpu_freq','')
    else:
       cmd=tosd.get('script_set_gpu_freq','').replace('$#freq#$',str(v))

    path_to_scripts=tosd.get('path_to_scripts','')
    if path_to_scripts!='': cmd=path_to_scripts+dir_sep+cmd

    if cmd!='':
       ck.out('')
       ck.out('CMD to set GPU frequency:')
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
