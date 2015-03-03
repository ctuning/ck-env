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


    o=i.get('out','')

    oo=''
    if o=='con': oo=o

    os=i.get('os','')
    device_id=i.get('device_id','')

    target={}

    # Get info about host/target OS and CPU at the same time
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.cpu'],
        'os':os,
        'device_id':device_id,
        'out':oo}
    rr=ck.access(ii)
    if rr['return']>0: return rr # Careful will be updating this rr

    os=rr['os_uoa']
    device_id=rr['device_id']

    host_name=rr['host']['name']

    os_uoa=rr['os_uoa']
    os_uid=rr['os_uid']
    os_dict=rr['os_dict']

    remote=os_dict.get('remote','')
    os_win=os_dict.get('windows_base','')

    # Get info about accelerator (GPU)
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.accelerator'],
        'os':os,
        'device_id':device_id,
        'out':oo}
    rx=ck.access(ii)
    if rx['return']>0: return rx # Careful will be updating this rr

    rr.update(rx)
    
    if remote=='yes':
       remote_init=os_dict.get('remote_init','')
    










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
       ck.out('System name:        '+target_system_name)
       ck.out('System model:       '+target_system_model)
       ck.out('')

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
