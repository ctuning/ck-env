#
# Collective Knowledge (checking and installing software)
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
# detect soft

def detect(i):
    """
    Input:  {
              (host_os)           - host OS (detect, if omitted)
              (target_os)         - target OS (detect, if omitted)
              (target_device_id)  - target device ID (detect, if omitted)

              (data_uoa) or (uoa) - environment UOA entry
               or
              (tags)              - search UOA by tags (separated by comma)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              version_str  - version as string
              version_lst  - version as list of strings
            }

    """

    import os

    o=i.get('out','')

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')

    # Checking/detecting host OS
    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'os':hos})
    if r['return']>0: return r
    hos=r['os_uid']
    hosd=r['os_dict']

    # Checking/detecting host OS
    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'os':tos,
                 'device_id':tdid})
    if r['return']>0: return r
    tos=r['os_uid']
    tosd=r['os_dict']
    tdid=r['device_id']

    # Check environment UOA
    duoa=i.get('uoa','')
    if duoa=='': duoa=i.get('data_uoa','')
    if duoa=='':
       # Search
       tags=i.get('tags','')

       if tags!='':
          r=ck.access({'action':'search',
                       'module_uoa':work['self_module_uid'],
                       'tags':tags})
          if r['return']>0: return r
          l=r['lst']
          if len(l)>0:
             duid=l[0].get('data_uid')
             duoa=duid

    if duoa=='':
       return {'return':1, 'error':'software entry was not found'}

    # Load
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa})
    if r['return']>0: return r
    d=r['dict']
    p=r['path']

    duoa=r['data_uoa']
    duid=r['data_uid']

    if o=='con':
       x=duoa
       if duid!=duoa: x+=' ('+duid+')'
       ck.out('Software entry found: '+x)

    # Check if has version
    ver=d.get('version','')
    cmd=ver.get('cmd','')
    lst=[]

    dver=''
    lver=[]

    if cmd!='':
       rx=ck.gen_tmp_file({})
       if rx['return']>0: return rx
       fn=rx['file_name']

       cmd=cmd.replace('$#filename#$', fn)
       ry=os.system(cmd)
#       if ry>0:
#          return {'return':16, 'error':'executing command returned non-zero value ('+cmd+')'}

       if os.path.isfile(fn): 
          rx=ck.load_text_file({'text_file':fn, 'split_to_list':'yes'})
          if rx['return']>0: return rx
          lst=rx['lst']

          os.remove(fn)

    if len(lst)==0:
       return {'return':16, 'error':'version output file is empty'}

    tp=ver.get('type','')
    if tp=='parse_first_string':
       s=lst[0]

       sbefore=ver.get('string_before','')
       safter=ver.get('string_after','')
       safter_rel=ver.get('string_after_relaxed','')

       i1=0
       i2=len(s)

       if sbefore!='':
          i1=s.find(sbefore)
          if i1<0: return {'return':16, 'error':'version was not parsed'}

       if safter!='':
          if sbefore!='': i2=s.find(safter, i1+len(sbefore)+1)
          else: i2=s.find(safter)

          if i2<0: return {'return':16, 'error':'version was not parsed'}
       elif safter_rel!='':
          if sbefore!='': i3=s.find(safter_rel, i1+len(sbefore)+1)
          else: i3=s.find(safter_rel)

          if i3>=0: i2=i3

       dver=s[i1+len(sbefore):i2].strip()

       spl=ver.get('split','')
       if spl!='':
          lver=dver.split(spl)

    if dver=='':
       return {'return':16, 'error':'version was not detected'}

    return {'return':0, 'version_str':dver, 'version_lst':lver}

##############################################################################
# setup environment

def setup(i):
    """
    Input:  {
              (host_os)           - host OS (detect, if omitted)
              (target_os)         - target OS (detect, if omitted)
              (target_device_id)  - target device ID (detect, if omitted)

              (data_uoa) or (uoa) - environment UOA entry
               or
              (tags)              - search UOA by tags (separated by comma)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              version_str  - version as string
              version_lst  - version as list of strings
            }

    """

    import os

    o=i.get('out','')

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')

    # Checking/detecting host OS
    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'os':hos})
    if r['return']>0: return r
    hos=r['os_uid']
    hosd=r['os_dict']

    # Checking/detecting host OS
    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'os':tos,
                 'device_id':tdid})
    if r['return']>0: return r
    tos=r['os_uid']
    tosd=r['os_dict']
    tdid=r['device_id']

    # Check environment UOA
    duoa=i.get('uoa','')
    if duoa=='': duoa=i.get('data_uoa','')
    if duoa=='':
       # Search
       tags=i.get('tags','')

       if tags!='':
          r=ck.access({'action':'search',
                       'module_uoa':work['self_module_uid'],
                       'tags':tags})
          if r['return']>0: return r
          l=r['lst']
          if len(l)>0:
             duid=l[0].get('data_uid')
             duoa=duid

    if duoa=='':
       return {'return':1, 'error':'software entry was not found'}

    # Load
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa})
    if r['return']>0: return r
    d=r['dict']
    p=r['path']

    duoa=r['data_uoa']
    duid=r['data_uid']

    if o=='con':
       x=duoa
       if duid!=duoa: x+=' ('+duid+')'
       ck.out('Software entry found: '+x)

    # Prepare first meta
    tbits=tosd.get('bits','')
    meta={"host_os":hos,
          "target_os":tos,
          "target_bits":tbits
         }

    misc={"host_os_dict":hosd,
          "target_os_dict":tosd,
          "target_device_id":tdid
         }

    # Check if script
    setup=d.get('setup',{})
    setup_script=setup.get('script','')

    if setup_script!='':
       # Check individual prepare script
       rx=ck.load_module_from_path({'path':p, 'module_code_name':setup_script, 'skip_init':'yes'})
       if rx['return']>0: return rx
       crx=rx['code']

       # Prepare info
       rx=ck.gen_tmp_file({})
       if rx['return']>0: return rx
       fn=rx['file_name']

       # Call setup script
       rx=crx.setup({"meta":meta, "misc":misc})
       if rx['return']>0: return rx











    exit(1)

    # Check if has version
    ver=d.get('version','')
    cmd=ver.get('cmd','')
    lst=[]

    dver=''
    lver=[]

    if cmd!='':
       rx=ck.gen_tmp_file({})
       if rx['return']>0: return rx
       fn=rx['file_name']

       cmd=cmd.replace('$#filename#$', fn)
       ry=os.system(cmd)
#       if ry>0:
#          return {'return':16, 'error':'executing command returned non-zero value ('+cmd+')'}

       if os.path.isfile(fn): 
          rx=ck.load_text_file({'text_file':fn, 'split_to_list':'yes'})
          if rx['return']>0: return rx
          lst=rx['lst']

          os.remove(fn)

    if len(lst)==0:
       return {'return':16, 'error':'version output file is empty'}

    tp=ver.get('type','')
    if tp=='parse_first_string':
       s=lst[0]

       sbefore=ver.get('string_before','')
       safter=ver.get('string_after','')
       safter_rel=ver.get('string_after_relaxed','')

       i1=0
       i2=len(s)

       if sbefore!='':
          i1=s.find(sbefore)
          if i1<0: return {'return':16, 'error':'version was not parsed'}

       if safter!='':
          if sbefore!='': i2=s.find(safter, i1+len(sbefore)+1)
          else: i2=s.find(safter)

          if i2<0: return {'return':16, 'error':'version was not parsed'}
       elif safter_rel!='':
          if sbefore!='': i3=s.find(safter_rel, i1+len(sbefore)+1)
          else: i3=s.find(safter_rel)

          if i3>=0: i2=i3

       dver=s[i1+len(sbefore):i2].strip()

       spl=ver.get('split','')
       if spl!='':
          lver=dver.split(spl)

    if dver=='':
       return {'return':16, 'error':'version was not detected'}

    return {'return':0, 'version_str':dver, 'version_lst':lver}
