#
# Collective Knowledge (environment)
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
# set environment for tools and libraries 
# (multiple versions of the same tools/libraries can co-exist)

def set(i):
    """
    Input:  {
              (host_os)          - host OS (detect, if ommitted)
              (target_os)        - target OS (detect, if ommitted)
              (target_device_id) - target device ID (detect, if omitted)

              (uoa)      - environment UOA entry
               or
              (tags)     - search UOA by tags (separated by comma)

              (bat_file) - if !='', use this filename to generate/append batch file ...
              (bat_new)  - if 'yes', start new bat file

              (env)      - existing environment
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

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
    if duoa=='':
       # Search
       tags=i.get('tags','')
       

       r=ck.access({'action':'search',
                    'module_uoa':work['self_module_uid'],
                    'tags':tags})
       if r['return']>0: return r
       l=r['lst']
       if len(l)>0:
          duid=l[0].get('data_uid')
          duoa=duid

          if o=='con':
             x=duoa
             if duid!=duoa: x+=' ('+duid+')'
             ck.out('Environment found: '+x)

    if duoa=='':
       return {'return':1, 'error':'environment was not found'}

    # Load
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa})
    if r['return']>0: return r
    d=r['dict']
    p=r['path']

    # Prepare environment and batch
    env=i.get('environment',[])
    batch=[]

    # Process CMD first:
    import os

    cmd=d.get('cmd',[])
    for q in cmd:
        s='call '+os.path.join(p,q)
        batch.append(s)

    # Process environment next:
    envx=d.get('env',{})
    for q in envx:
        print q


    # Check batch file

    bf=i.get('bat_file','')

    if bf!='':
       bn=i.get('bat_new','')
       x='a'
       if bn=='yes': x='w'

       fbf=open(bf, x)

       # Check first, if CMD:
       for q in batch:
           fbf.write(q+'\n')

       fbf.close()

    return {'return':0, 'env':env, 'env_batch':batch}
