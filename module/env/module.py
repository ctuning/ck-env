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

              (local) - if 'yes', add host_os, target_os, target_device_id to search

              (bat_file) - if !='', use this filename to generate/append bat file ...
              (bat_new)  - if 'yes', start new bat file

              (env)      - existing environment

              (print)    - if 'yes', print found environment
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              env_uoa      - found environment UOA
              env          - updated environment
              bat          - string for bat file
              len          - number of found entries
            }

    """

    o=i.get('out','')

    # Clean output file
    import os

    bf=i.get('bat_file','')
    if bf!='' and os.path.isfile(bf): os.remove(bf)

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

    tbits=tosd.get('bits','')

    # Check environment UOA
    duoa=i.get('uoa','')
    lx=0
    if duoa=='':
       # Search
       tags=i.get('tags','')
       
       ii={'action':'search',
           'module_uoa':work['self_module_uid'],
           'tags':tags,
           'add_meta':'yes'} # Need to sort by version, if ambiguity

       if i.get('local','')=='yes':
          setup={'host_os_uoa':hos,
                 'target_os_uoa':tos,
                 'target_os_bits':tbits}
          ii['search_dict']={'setup':setup}

       r=ck.access(ii)
       if r['return']>0: return r
       l=r['lst']
       lx=len(l)
       if lx>0:
          if lx>1:
             ls=sorted(l, key=lambda k: k.get('meta',{}).get('misc',{}).get('version_int',0), reverse=True)
             l=ls

          duid=l[0].get('data_uid')
          duoa=duid

          if o=='con' and i.get('print','')=='yes':
             x=duoa
             if duid!=duoa: x+=' ('+duid+')'
             ck.out('CK environment found using tags "'+tags+'" : '+x)

    if duoa=='':
       return {'return':1, 'error':'environment was not found using tags "'+tags+'"'}

    # Load
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa})
    if r['return']>0: return r
    d=r['dict']
    p=r['path']

    # Prepare environment and bat
    env=i.get('env',{})
    xenv=d.get('env',{})
    env.update(xenv)

    # Process CMD first:
    sb=''

    es=d.get('env_script','')
    if es!='':
       sb+='call '+os.path.join(p,es)+'\n'

    # Check bat file
    if bf!='':
       bn=i.get('bat_new','')
       x='a'
       if bn=='yes': x='w'

       try:
          fbf=open(bf, x)
          fbf.write(sb)
       except Exception as e: 
          fbf.close()
          return {'return':1, 'error':'problem writing environment file ('+format(e)+')'}

       fbf.close()

    return {'return':0, 'env_uoa':duoa, 'env':env, 'bat':sb, 'len':lx}

##############################################################################
# show all installed environment

def show(i):
    """
    Input:  {
              (repo_uoa)          - repository UOA (with wildcards)
              (module_uoa)        - module UOA (with wildcards)
              (data_uoa)          - data UOA (with wildcards)

              (tags)              - prune by tags
              (target_os)         - prune by target OS
              (target_bits)       - prune by target bits
              (version)           - prune by version
              (name)              - prune by name with wildcards
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              lst          - list from search function
              view         - sorted view list
            }

    """

    o=i.get('out','')

    ruoa=i.get('repo_uoa','')
    muoa=i.get('module_uoa','')
    duoa=i.get('data_uoa','')

    tags=i.get('tags','')

    tos_uoa=i.get('target_os','')
    if tos_uoa!='':
       # Load OS
       ry=ck.access({'action':'load',
                     'module_uoa':cfg['module_deps']['os'],
                     'data_uoa':tos_uoa})
       if ry['return']>0: return ry
       tags+='target-os-'+ry['data_uoa']

    tb=i.get('target_bits','')
    if tb!='':
       tags+=tb+'bits'

    ver=i.get('version','')
    if ver!='':
       tags+='v'+ver

    name=i.get('name','')
    wname=False
    if name.find('*')>=0 or name.find('?')>=0:
       import fnmatch
       wname=True 
       name=name.lower()

    ii={'action':'search',
        'module_uoa':muoa,
        'repo_uoa':ruoa,
        'data_uoa':duoa,
        'tags':tags,
        'add_info':'yes',
        'add_meta':'yes'}
    rx=ck.access(ii)
    if rx['return']>0: return rx

    lst=rx['lst']

    # prepare view
    view=[]
    
    lv={} # length of each field

    target_os_name={} # Caching target OS names

    for q in lst:
        vv={}

        duoa=q['data_uoa']
        duid=q['data_uid']

        ruoa=q['repo_uoa']
        ruid=q['repo_uid']

        info=q['info']
        meta=q['meta']

        misc=meta.get('misc',{})
        setup=meta.get('setup','')
        tags=meta.get('tags',[])

        host_os_uoa=setup.get('host_os_uoa','')
        target_os_uoa=setup.get('target_os_uoa','')
        tbits=setup.get('target_os_bits','')
        version=setup.get('version','')
        version_int=misc.get('version_int',0)

        dname=info.get('data_name','')

        add=True
        if name!='':
           if wname:
              if not fnmatch.fnmatch(dname.lower(), name):
                 add=False
           else:
              if name!=dname:
                 add=False

        if add:
           # Check target OS
           if target_os_uoa in target_os_name:
              tduoa=target_os_name[target_os_uoa]
           else:
              # Load
              ry=ck.access({'action':'load',
                            'module_uoa':cfg['module_deps']['os'],
                            'data_uoa':target_os_uoa})
              if ry['return']>0: return ry
              tduoa=ry['data_uoa']
              target_os_name[target_os_uoa]=tduoa

           stags=''
           for t in tags:
               if t!='':
                  if stags!='': stags+=','
                  stags+=t

           vv['data_uid']=duid
           vv['repo_uid']=ruid
           vv['tags']=stags
           vv['host_os_uoa']=host_os_uoa
           vv['target_os_uoa']=tduoa
           vv['tbits']=tbits
           vv['version']=version
           vv['version_int']=version_int
           vv['data_name']=dname

           # Check length
           for k in vv:
               v=str(vv[k])
               l=len(v)
               if k not in lv: lv[k]=l
               elif l>lv[k]: lv[k]=l

           view.append(vv)

    # Sort by target_os_uoa, name and version_int
    vs=sorted(view, key=lambda k: (k['target_os_uoa'],
                                   k['tbits'],
                                   k['data_name'],
                                   k['version_int']))

    # Print
    if o=='con':
       if len(vs)>0:
          # Headers
          sh ='Env UID:' + (' ' * (lv['data_uid']- 8))
          sh+=' Target OS:' + (' ' * (lv['target_os_uoa']-10))
          sh+=' Bits:'
          sh+=' Name:' + (' ' * (lv['data_name']- 5))
          sh+=' Version:' + (' ' * (lv['version']- 8))
          sh+=' Tags:'

          ck.out(sh)

          for q in vs:
              x=q['data_uid']
              sh=(' ' * (lv['data_uid']- len(x))) + x

              x=q['target_os_uoa']
              sh+=' '+(' ' * (lv['target_os_uoa']- len(x))) + x

              x=q['tbits']
              sh+=' '+(' ' * (5 - len(x))) + x

              x=q['data_name']
              sh+=' '+ x + (' ' * (lv['data_name']- len(x)))
       
              x=q['version']
              sh+=' '+(' ' * (8 - len(x))) + x

              x=q['tags']
              sh+=' '+x

              ck.out(sh)

    return {'return':0, 'lst':lst, 'view':vs}

##############################################################################
# resolve all dependencies

def resolve(i):
    """
    Input:  {
              (host_os)          - host OS (detect, if ommitted)
              (target_os)        - target OS (detect, if ommitted)
              (target_device_id) - target device ID (detect, if omitted)

              deps               - dependencies

              (env)              - env
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - string for bat file calling all bats ...
              deps         - updated deps (with uoa)
              env          - updated env
              res_deps     - list of UOAs (resolved dependencies)
            }

    """

    sb=''

    deps=i.get('deps',{})

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
    
    # Checking deps
    ndeps=[]
    env=i.get('env',{})

    res=[]
    for q in deps:
        import copy
        qq=copy.deepcopy(q)
        
        name=q.get('name','')
        tags=q.get('tags','')
        local=q.get('local','')

        rx=set({'host_os':hos,
                'target_os':tos,
                'target_device_id':tdid,
                'tags':tags,
                'env':env,
                'local':local
               })
        if rx['return']>0: return rx

        lx=rx['len']

        uoa=rx['env_uoa']
        qq['uoa']=uoa
        qq['num_entries']=lx

        ndeps.append(qq)

        if uoa not in res: res.append(uoa)

        env=rx['env']
        
        sb+=rx['bat']

    return {'return':0, 'deps':ndeps, 'env': env, 'bat':sb, 'res_deps':res}
