#
# Collective Knowledge (environment)
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
# set environment for tools and libraries 
# (multiple versions of the same tools/libraries can co-exist)

def set(i):
    """
    Input:  {
              (host_os)              - host OS (detect, if ommitted)
              (target_os)            - target OS (detect, if ommitted)
              (target_device_id)     - target device ID (detect, if omitted)

              (repo_uoa)             - repo where to limit search

              (uoa)                  - environment UOA entry
               or
              (tags)                 - search UOA by tags (separated by comma)

              (local)                - if 'yes', add host_os, target_os, target_device_id to search

              (deps)                 - already resolved deps
              (skip_auto_resolution) - if 'yes', do not check if deps are already resolved

              (bat_file)             - if !='', use this filename to generate/append bat file ...
              (bat_new)              - if 'yes', start new bat file

              (env)                  - existing environment

              (print)                - if 'yes', print found environment
            }

    Output: {
              return       - return code =  0, if successful
                                         = 32, if environment was deleted (env_uoa - env which was not found)
                                         >  0, if error
              (error)      - error text if return > 0

              env_uoa      - found environment UOA
              env          - updated environment
              bat          - string for bat file
              lst          - all found entries
              dict         - meta of the selected env entry
            }

    """

    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    # Clean output file
    import os

    sar=i.get('skip_auto_resolution','')
    cdeps=i.get('deps',{})

    bf=i.get('bat_file','')
    if bf!='' and os.path.isfile(bf): os.remove(bf)

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')

    user_env=False
    if hos!='' or tos!='' or tdid!='': user_env=True

    # Checking/detecting host OS
    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'os':hos,
                 'skip_info_collection':'yes'})
    if r['return']>0: return r
    hos=r['os_uid']
    hosd=r['os_dict']

    # Checking/detecting host OS
    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'os':tos,
                 'device_id':tdid,
                 'skip_info_collection':'yes'})
    if r['return']>0: return r
    tos=r['os_uid']
    tosd=r['os_dict']
    tdid=r['device_id']

    # Check if base is different
    x1=hosd.get('base_uid','')
    x2=hosd.get('base_uoa','')
    if x1!='' and x2!='': 
       hos=x1
       hosx=x2
    x1=tosd.get('base_uid','')
    x2=tosd.get('base_uoa','')
    if x1!='' and x2!='': 
       tos=x1
       tosx=x2

    tbits=tosd.get('bits','')

    # Check environment UOA
    enruoa=i.get('repo_uoa','')

    tags=i.get('tags','')
    duoa=i.get('uoa','')
    lx=0
    dd={}
    setup={}

    # Search
    ii={'action':'search',
        'module_uoa':work['self_module_uid'],
        'tags':tags,
        'repo_uoa':enruoa,
        'data_uoa':duoa,
        'add_info':'yes',
        'add_meta':'yes'} # Need to sort by version, if ambiguity

    if user_env or i.get('local','')=='yes':
       setup={'host_os_uoa':hos,
              'target_os_uoa':tos,
              'target_os_bits':tbits}
       ii['search_dict']={'setup':setup}

    r=ck.access(ii)
    if r['return']>0: return r
    l=r['lst']
    lx=len(l)
    if lx>0:
       ilx=0
       if lx>1 and sar!='yes':
          # Try auto-resolve or prune choices
          nls=[]
          for z in range(0, lx):
              j=l[z]
              zm=j.get('meta',{})
              cus=zm.get('customize','')
              zdeps=zm.get('deps',{})


              skip=False
              for q in zdeps:
                  jj=zdeps[q]
                  juoa=jj.get('uoa','')

                  for a in cdeps:
                      if a==q:
                         aa=cdeps[a]
                         auoa=aa.get('uoa','')

                         if auoa!=juoa:
                            skip=True
                            break

                  if skip: break
              if not skip: nls.append(j)    

          l=nls
          lx=len(l)

       # Choose sub-deps
       if lx>1:
          ls=sorted(l, key=lambda k: k.get('meta',{}).get('misc',{}).get('version_int',0), reverse=True)
          l=ls

          if o=='con':
             xq='tags="'+tags+'"'
             if len(setup)>0:
                import json

                ro=readable_os({'setup':setup})
                if ro['return']>0: return ro
                setup1=ro['setup1']

                xq+=' and setup='+json.dumps(setup1)

             ck.out('')
             ck.out('More than one environment found for '+xq+':')
             ck.out('')
             zz={}
             for z in range(0, lx):
                 j=l[z]

                 zi=j.get('info',{})
                 zm=j.get('meta',{})
                 zu=j.get('data_uid','')
                 zdn=zi.get('data_name','')
                 cus=zm.get('customize','')
                 zdeps=zm.get('deps',{})
                 xsetup=zm.get('setup',{})
                 xtags=zm.get('tags','')
                 ver=cus.get('version','')

                 xtarget_os_uoa=xsetup.get('target_os_uoa','')

                 xstags=''
                 for t in xtags:
                     if t!='':
                        if xstags!='': xstags+=','
                        xstags+=t

                 zs=str(z)
                 zz[zs]=zu

                 ck.out('')
                 ck.out(zs+') '+zdn+' - v'+ver+' ('+xstags+' ('+zu+'))')

                 if len(zdeps)>0:
                    for j in sorted(zdeps, key=lambda v: zdeps[v].get('sort',0)):
                        jj=zdeps[j]
                        juoa=jj.get('uoa','')
                        jtags=jj.get('tags','')
                        jver=jj.get('ver','')

                        js='                                  '
                        js+='Dependency '+j+' (UOA='+juoa+', tags="'+jtags+'", version='+jver+')'
                        ck.out(js)



             ck.out('')
             rx=ck.inp({'text':'Choose first number to resolve dependency for '+xq+' or press Enter for 0: '})
             x=rx['string'].strip()

             if x=='': x='0'

             if x not in zz:
                return {'return':1, 'error':'dependency number is not recognized'}

             ilx=int(x)

       if ilx<len(l):
          duid=l[ilx].get('data_uid')
          duoa=duid

          dd=l[ilx].get('meta',{})

          if o=='con' and i.get('print','')=='yes':
             x=duoa
             if duid!=duoa: x+=' ('+duid+')'
             ck.out('CK environment found using tags "'+tags+'" : '+x)

    if duoa=='':
       import json
       x='environment was not found using tags="'+tags+'"'
       if len(setup)>0:

          ro=readable_os({'setup':setup})
          if ro['return']>0: return ro
          setup1=ro['setup1']

          x+=' and setup='+json.dumps(setup1)

       if o=='con' and tags!='':
          ck.out('')
          ck.out('==========================================================================================')
          ck.out('WARNING: '+x)
          ck.out('')
          rx=ck.inp({'text':'  Would you like to search and install package with these tags automatically (Y/n)? '})
          a=rx['string'].strip().lower()

          if a!='n' and a!='no':
             save_cur_dir=os.getcwd()

             vv={'action':'install',
                 'module_uoa':cfg['module_deps']['package'],
                 'out':oo,
                 'tags':tags}
             vv['host_os']=hos
             vv['target_os']=tos
             vv['target_device_id']=tdid

             # Check if there is a compiler in resolved deps to reuse it
             xdeps={}
#             if len(cdeps.get('compiler',{}))>0: xdeps['compiler']=cdeps['compiler']
             if cdeps.get('compiler',{}).get('uoa','')!='': xdeps['compiler']=cdeps['compiler']
#             if len(cdeps.get('compiler_mcl',{}))>0: xdeps['compiler_mcl']=cdeps['compiler_mcl']
             if cdeps.get('compiler_mcl',{}).get('uoa','')!='': xdeps['compiler_mcl']=cdeps['compiler_mcl']
             if len(xdeps)>0: vv['deps']=xdeps

             rx=ck.access(vv)
             if rx['return']>0: return rx

             duoa=rx['env_data_uoa']
             duid=rx['env_data_uid']

             os.chdir(save_cur_dir)

          else:
             return {'return':1, 'error':x}
       else:
          return {'return':1, 'error':x}

    # Load selected environment entry
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa})
    if r['return']>0: 
       if r['return']==16:
          r['return']=32
          r['env_uoa']=duoa
       return r
    d=r['dict']
    p=r['path']

    # Prepare environment and bat
    env=i.get('env',{})
    xenv=d.get('env',{})
    env.update(xenv)

    env_call=hosd.get('env_call','')
    bin_prefix=hosd.get('bin_prefix','')

    # Process CMD first:
    sb=''

    es=d.get('env_script','')
    if es!='':
       sb+=env_call+' '+os.path.join(p,es)+'\n'

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

    return {'return':0, 'env_uoa':duoa, 'env':env, 'bat':sb, 'lst':l, 'dict':d}

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

       tos_uoa=ry['data_uoa']
       tosz=ry['dict'].get('base_uoa','')
       if tosz!='': tos_uoa=tosz

       if tags!='': tags+=','
       tags+='target-os-'+tos_uoa

    tb=i.get('target_bits','')
    if tb!='':
       if tags!='': tags+=','
       tags+=tb+'bits'

    ver=i.get('version','')
    if ver!='':
       if tags!='': tags+=','
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

        cus=meta.get('customize',{})
        setup=meta.get('setup','')
        tags=meta.get('tags',[])

        host_os_uoa=setup.get('host_os_uoa','')
        target_os_uoa=setup.get('target_os_uoa','')
        tbits=setup.get('target_os_bits','')
        version=setup.get('version','')
        version_int=cus.get('version_int',0)

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

           if lv['data_name']<5: lv['data_name']=5
           if lv['target_os_uoa']<10: lv['target_os_uoa']=10
           if lv['version']<8: lv['version']=8

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

          ck.out('')
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
              sh+=' '+ x + (' ' * (lv['version'] - len(x)))

              x=q['tags']
              sh+=' '+x

              ck.out(sh)

    return {'return':0, 'lst':lst, 'view':vs}

##############################################################################
# resolve all dependencies

def resolve(i):
    """
    Input:  {
              (host_os)              - host OS (detect, if ommitted)
              (target_os)            - target OS (detect, if ommitted)
              (target_device_id)     - target device ID (detect, if omitted)

              (repo_uoa)             - repo where to limit search

              deps                   - dependencies dict

              (env)                  - env

              (add_customize)        - if 'yes', add to deps customize field from the environment 
                                       (useful for program compilation)

              (skip_dict)            - if 'yes', do not add to deps dict field from the environment 
                                       (useful for program compilation)

              (skip_auto_resolution) - if 'yes', do not check if deps are already resolved
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - string for bat file calling all bats ...
              cut_bat      - string for bat file calling all bats (dos not include deps that are explicitly excluded) ...
              deps         - updated deps (with uoa)
              env          - updated env
            }

    """

    o=i.get('out','')

    if o=='con':
       ck.out('')
       ck.out('Resolving dependencies ...')

    sb=''
    sb1=''

    sar=i.get('skip_auto_resolution','')

    deps=i.get('deps',{})

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')

    # Checking/detecting host OS
    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'os':hos,
                 'skip_info_collection':'yes'})
    if r['return']>0: return r
    hos=r['os_uid']
    hosd=r['os_dict']

    # Checking/detecting host OS
    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'os':tos,
                 'device_id':tdid,
                 'skip_info_collection':'yes'})
    if r['return']>0: return r
    tos=r['os_uid']
    tosd=r['os_dict']
    tdid=r['device_id']

    # Check if base is different
    x1=hosd.get('base_uid','')
    x2=hosd.get('base_uoa','')
    if x1!='' and x2!='': 
       hos=x1
       hosx=x2
    x1=tosd.get('base_uid','')
    x2=tosd.get('base_uoa','')
    if x1!='' and x2!='': 
       tos=x1
       tosx=x2

    # Checking deps
    env=i.get('env',{})

    enruoa=i.get('repo_uoa','')

    ac=i.get('add_customize','')
    sd=i.get('skip_dict','')

    res=[]
    for k in sorted(deps, key=lambda v: deps[v].get('sort',0)):
        q=deps[k]

        tags=q.get('tags','')
        local=q.get('local','')

        uoa=q.get('uoa','')

        ii={'host_os':hos,
            'target_os':tos,
            'target_device_id':tdid,
            'tags':tags,
            'repo_uoa':enruoa,
            'env':env,
            'uoa':uoa,
            'deps':deps,
            'skip_auto_resolution':sar,
            'local':local
           }
        if o=='con': ii['out']='con'
        rx=set(ii)
        if rx['return']>0: return rx

        lst=rx['lst']
        dd=rx['dict']

        # add choices
        zchoices=[]
        for zw in lst:
            zchoices.append(zw['data_uid'])

        if 'choices' not in q or len('choices')==0: 
           q['choices']=zchoices

        cus=dd.get('customize',{})

        if ac=='yes': q['cus']=cus
        if sd!='yes': q['dict']=dd

        ver=cus.get('version','')
        if ver!='': q['ver']=ver

        uoa=rx['env_uoa']
        q['uoa']=uoa
        q['num_entries']=len(lst)

        bdn=cus.get('build_dir_name','')
        if bdn!='': q['build_dir_name']=bdn # Needed to suggest directory name for building libs

        if uoa not in res: res.append(uoa)

        env=rx['env']

        bt=rx['bat']

        q['bat']=bt
        sb+=bt

        if q.get('skip_from_bat','')!='yes':
           sb1+=bt

    return {'return':0, 'deps':deps, 'env': env, 'bat':sb, 'cut_bat':sb1, 'res_deps':res}

##############################################################################
# refresh environment (re-setup soft)

def refresh(i):
    """
    Input:  {
              (repo_uoa)          - repository UOA (with wildcards), default = local (to avoid updating other repos)
              (module_uoa)        - module UOA (with wildcards)
              (data_uoa)          - data UOA (with wildcards)

              (tags)              - prune by tags
              (target_os)         - prune by target OS
              (target_bits)       - prune by target bits
              (version)           - prune by version
              (name)              - prune by name with wildcards

              (reset_env)         - if 'yes', do not use environment from existing entry, but use original one
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
    if ruoa=='': ruoa='local'

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
       tos_uoa=ry['data_uoa']
       tosz=ry['dict'].get('base_uoa','')
       if tosz!='': tos_uoa=tosz
       tags+='target-os-'+tos_uoa

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

        cus=meta.get('customize',{})
        deps=meta.get('deps',{})
        setup=meta.get('setup','')
        tags=meta.get('tags',[])

        sftags=''
        for t in tags:
            if t!='':
               if sftags!='': sftags+=','
               sftags+=t

        host_os_uoa=setup.get('host_os_uoa','')
        target_os_uoa=setup.get('target_os_uoa','')
        tbits=setup.get('target_os_bits','')
        version=setup.get('version','')
        version_int=cus.get('version_int',0)

        dname=info.get('data_name','')

        ck.out('***********************************************************************')
        ck.out(dname+' (Env: '+duid+')')

        ck.out('')
        ck.out('  Tags="'+sftags+'"')

        soft_uoa=meta.get('soft_uoa','')
        if soft_uoa=='':
           # Trying to detect by some tags
           tagsx=[]
           for q in tags:
               if not q.startswith('host-os-') and not q.startswith('target-os-') and \
                  not q.endswith('bits') and not q.startswith('v') and \
                  q!='retargeted':
                  tagsx.append(q)

           stags=''
           for t in tagsx:
               if t!='':
                  if stags!='': stags+=','
                  stags+=t

           ck.out('  All tags="'+sftags+'"')
           ck.out('  Searching soft UOA by tags="'+stags+'" ...')

           rx=ck.access({'action':'search',
                         'module_uoa':cfg['module_deps']['soft'],
                         'tags':stags})
           if rx['return']>0: return rx

           lst=rx['lst']
           if len(lst)==0:
              ck.out('')
              ck.out('  No soft found')

              rx=ck.inp({'text':'  Please, enter soft UOA: '})
              soft_uoa=rx['string'].strip()
           elif len(lst)==1:
              soft_uoa=lst[0]['data_uid']
              ck.out('     Unique soft UOA found='+lst[0]['data_uoa'])
           else:
              ck.out('')
              ck.out('  Available soft for these tags:')
              num={}
              ix=0
              for q in lst:
                  num[str(ix)]=q['data_uid']
                  ck.out('     '+str(ix)+') '+q['data_uoa'])
                  ix+=1

              rx=ck.inp({'text':'  Choose first number to select soft UOA: '})
              x=rx['string'].strip()

              if x not in num:
                 return {'return':1, 'error':'number is not found'}

              soft_uoa=num[x]

           meta['soft_uoa']=soft_uoa

           # Update environment entry
           rx=ck.access({'action':'update',
                         'module_uoa':work['self_module_uid'],
                         'data_uoa':duoa,
                         'dict':meta,
                         'sort_keys':'yes'})
           if rx['return']>0: return rx

        # Check if package available to take env
        penv={}
        package_uoa=meta.get('package_uoa','')
        if package_uoa!='':
           ck.out('')
           ck.out('  Related package: '+package_uoa)

           rx=ck.access({'action':'load',
                         'module_uoa':cfg['module_deps']['package'],
                         'data_uoa':package_uoa})
           if rx['return']>0: return rx
           pdd=rx['dict']
           penv=pdd.get('env',{})

        # Trying new setup
        ck.out('')
        ck.out('  Refreshing setup ...')

        ii={'action':'setup',
            'module_uoa':cfg['module_deps']['soft'],
            'host_os':host_os_uoa,
            'target_os':target_os_uoa,
            'data_uoa':soft_uoa,
            'customize':cus,
            'deps':deps,
            'package_uoa':package_uoa,
            'env':penv,
            'env_data_uoa':duid}
        if i.get('reset_env','')!='': ii['reset_env']=i['reset_env']
        rx=ck.access(ii)
        if rx['return']>0: 
           if rx['return']!=32:
              return rx
           if o=='con':
              ck.out('')
              ck.out('One of the dependencies is missing for this setup!')
              ry=ck.inp({'text':'Would you like to delete it (Y/n)? '})
              x=ry['string'].strip().lower()
              if x!='n' and x!='no':
                 ry=ck.access({'action':'delete',
                               'module_uoa':work['self_module_uid'],
                               'data_uoa':duid})
                 if ry['return']>0: return ry
           else:
              return rx

    return {'return':0}

##############################################################################
# internal function to convert host_os and target_os from UID to UOA to be readable

def readable_os(i):
    """
    Input:  {
              setup 
                (host_os_uoa)    - UID or UOA
                (target_os_uoa)  - UID or UOA
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              setup1       - processed setup with host_os_uoa and target_os_uoa as UOA
            }
    """

    setup=i.get('setup',{})

    import copy
    setup1=copy.deepcopy(setup)

    x=setup.get('host_os_uoa','')
    if x!='':
       r=ck.access({'action':'load',
                    'module_uoa':cfg['module_deps']['os'],
                    'data_uoa':x})
       if r['return']>0: return r
       setup1['host_os_uoa']=r['data_uoa']

    x=setup.get('target_os_uoa','')
    if x!='':
       r=ck.access({'action':'load',
                    'module_uoa':cfg['module_deps']['os'],
                    'data_uoa':x})
       if r['return']>0: return r
       setup1['target_os_uoa']=r['data_uoa']

    return {'return':0, 'setup1':setup1}
