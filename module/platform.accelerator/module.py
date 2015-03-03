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

    o=i.get('out','')

    os=i.get('os','')
    device_id=i.get('device_id','')

    # Get info about host/target OS
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.os'],
        'os':os,
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

    if remote=='yes':
       remote_init=os_dict.get('remote_init','')
    










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
          q1=target_os_name_short.find('-')
          if q1>=0:
             target_os_name_short=target_os_name_short[0:q1]

          x1=''
          x2=''

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

    if o=='con':
       ck.out('GPU name: '+str(target_gpu_name))
       ck.out('')

    rr['gpu_properties_unified']=target

    return rr
