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
                     or
              (device_id)

              (repo_uoa)             - repo where to limit search

              (uoa)                  - environment UOA entry
               or
              (tags)                 - search UOA by tags (separated by comma)

              (or_tags)              - add entries which has groups of tags separated by ;
              (no_tags)              - exclude entris with these tags separated by comma

              (local)                - if 'yes', add host_os, target_os, target_device_id to search

              (key)                  - key from deps (to set env with path)
              (name)                 - user-friendly name of the dependency (if needs to be resolved)

              (deps)                 - already resolved deps

              (reuse_deps)           - if 'yes' reuse all deps if found in cache by tags
              (deps_cache)           - list with resolved deps
              (skip_cache)           - skip caching (sometimes needed to iterate over deps such as DNN libs
                                         during autotuning, crowd-benchmarking and crowd-tuning)

              (skip_auto_resolution)       - if 'yes', do not check if deps are already resolved
              (skip_default)               - if 'yes', skip detection of default installed software version
              (skip_installed)             - dict to specify on which platforms not to search already installed version
              (skip_pruning_by_other_deps) - if 'yes', do not prune available envs using other resolved deps

              (bat_file)             - if !='', use this filename to generate/append bat file ...
              (bat_new)              - if 'yes', start new bat file

              (env)                  - existing environment

              (print)                - if 'yes', print found environment

              (random)               - if 'yes' and there is a choice, select random
                                       (useful for quiet experiment crowdsourcing such as sw/hw crowdtuning)

              (quiet)                - if 'yes', automatically provide default answer to all questions when resolving dependencies ... 

              (force_env_init)       - if 'yes', add '1' when calling env script (useful for LLVM plugins for example to force reinit)

              (install_to_env)       - install dependencies to env instead of CK-TOOLS (to keep it clean)!

              (install_env)          - customize installation (useful for replay to rebuild proper package with external env)

              (version_from)         - check version starting from ... (list of numbers)
              (version_to)           - check version up to ... (list of numbers)

              (safe)                 - safe mode when searching packages first instead of detecting already installed soft
                                       (to have more deterministic build)

              (package_uoa)          - force installation package
                                       (also useful to rebuild deps during replay)
            }

    Output: {
              return           - return code =  0, if successful
                                             = 32, if environment was deleted (env_uoa - env which was not found)
                                             >  0, if error
              (error)          - error text if return > 0

              env_uoa          - found environment UOA
              env              - updated environment
              bat              - string for bat file
              lst              - all found entries
              dict             - meta of the selected env entry
              detected_version - detected version of a software
            }

    """

    import os
    import copy
    import json

    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    ran=i.get('random','')
    quiet=i.get('quiet','')

    name=i.get('name','')

    skip_cache=i.get('skip_cache','')

    package_uoa=i.get('package_uoa','')

    install_env=i.get('install_env',{})

    # Clean output file
    sar=i.get('skip_auto_resolution','')
    cdeps=i.get('deps',{})

    deps_cache=i.get('deps_cache',[])
    reuse_deps=i.get('reuse_deps','')

    skip_default=i.get('skip_default','')
    skip_installed=i.get('skip_installed',{})

    iev=i.get('install_to_env','')
    safe=i.get('safe','')

    bf=i.get('bat_file','')
    if bf!='' and os.path.isfile(bf): os.remove(bf)

    vfrom=i.get('version_from',[])
    vto=i.get('version_to',[])

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')
    if tdid=='': tdid=i.get('device_id','')

    user_env=False
    if hos!='' or tos!='' or tdid!='': user_env=True

    # Get some info about OS
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.os'],
        'host_os':hos,
        'target_os':tos,
        'device_id':tdid,
        'skip_info_collection':'yes'}
    r=ck.access(ii)
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    ck_os_name=hosd['ck_name']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

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

    remote=tosd.get('remote','')

    tbits=tosd.get('bits','')

    hplat=hosd.get('ck_name','')

    tplat2=i.get('original_target_os_name2','')

    eset=hosd.get('env_set','')
    svarb=hosd.get('env_var_start','')
    svare=hosd.get('env_var_stop','')
    sdirs=hosd.get('dir_sep','')
    evs=hosd.get('env_var_separator','')
    eifs=hosd.get('env_quotes_if_space','')
    nout=hosd.get('no_output','')

    # Check environment UOA
    enruoa=i.get('repo_uoa','')
    tags=i.get('tags','')
    or_tags=i.get('or_tags','')
    no_tags=i.get('no_tags','')
    duoa=i.get('uoa','')

    lx=0
    dd={}
    setup={}

    # Search
    ii={'action':'search',
        'module_uoa':work['self_module_uid'],
        'tags':tags,
        'repo_uoa':enruoa,
        'add_info':'yes',
        'add_meta':'yes'} # Need to sort by version, if ambiguity

    if user_env or i.get('local','')=='yes':
       setup={'host_os_uoa':hos,
              'target_os_uoa':tos,
              'target_os_bits':tbits}
       ii['search_dict']={'setup':setup}

    if reuse_deps=='yes' and skip_cache!='yes':
       # Check in cache!
       dmatch={'setup':setup, 'tags':tags.split(',')}
       for q in deps_cache:
           d1=q.get('meta',{})
           r=ck.compare_dicts({'dict1':d1, 'dict2':dmatch})
           if r['return']>0: return r
           if r['equal']=='yes':
              duoa=q.get('uoa','')
              reuse_deps='no' # to avoid updating cache
              break

    ii['data_uoa']=duoa

    iii=copy.deepcopy(ii) # may need to repeat after registration

    # Prepare possible warning
    x='required software '
    if name!='': x='"'+name+'"'
    war='no registered CK environment was found for '+x+' dependency with tags="'+tags+'"'

    if no_tags!='':
       war+=', no_tags="'+no_tags+'"'

    if len(setup)>0:
       ro=readable_os({'setup':setup})
       if ro['return']>0: return ro
       setup1=ro['setup1']

       war+=' and setup='+json.dumps(setup1)

    if len(vfrom)>0 or len(vto)>0:
       war+=' and version constraints ('+json.dumps(vfrom)+' <= v <= '+json.dumps(vto)+')'

    # Search for environment entries
    r=ck.access(ii)
    if r['return']>0: return r

    # Prune if needed
    r=prune_search_list({'lst':r['lst'], 
                         'or_tags':or_tags, 
                         'no_tags':no_tags, 
                         'version_from':vfrom, 
                         'version_to':vto})
    if r['return']>0: return r
    sbov=r.get('skipped_because_of_version','')

    l=r['lst']
    lx=len(l)

    auoas=[]

    dname=''

    try_to_reinstall=False
    if lx==0 and duoa!='':
       # Check exact problem
       rx=ck.access({'action':'load',
                     'module_uoa':work['self_module_uid'],
                     'data_uoa':duoa})
       if rx['return']>0:
          if rx['return']!=16: return rx

          if package_uoa=='':
             rx['error']='strange - missing environment ('+duoa+') and package not specified (may happen during replay from another machine)'

             if o=='con' and quiet!='yes':
                ck.out('')
                ck.out('    WARNING: '+rx['error']+'!')
                ck.out('')
#                ry=ck.inp({'text':'    Would you like to detect / reinstall again (Y/n)? '})
#                x=ry['string'].strip()
#
#                if x=='n' or x=='no':
#                   return rx
          else:
             # Otherwise can try to rebuild from provided package UOA
             ck.out('')
             ck.out('WARNING: environment doesn\'t exist but package provided - trying to redetect/reinstall ...')

          duoa=''
          iii['data_uoa']=duoa # since will be later new search
          l=[]
          lx=0

          try_to_reinstall=True

          # Repeat search if has without data uoa
          r=ck.access(iii)
          if r['return']>0: return r

          # Prune if needed
          r=prune_search_list({'lst':r['lst'], 
                               'or_tags':or_tags, 
                               'no_tags':no_tags, 
                               'version_from':vfrom, 
                               'version_to':vto,
                               'package_uoa':package_uoa})
          if r['return']>0: return r
          sbov=r.get('skipped_because_of_version','')

          l=r['lst']
          lx=len(l)

          auoas=[]

          dname=''

       if not try_to_reinstall:
          dds=rx['dict'].get('setup',{})

          # Changed setup
          if o=='con':
             ck.out('')
             ck.out('WARNING: requested host or target OS info is not matching info in env '+duoa+'!')

             ck.out('')
             rx=ck.access({'action':'convert_uid_to_alias', 'module_uoa':cfg['module_deps']['os'], 'uoa':dds.get('host_os_uoa','')})
             if rx['return']>0: return rx
             x=rx['string']
             ck.out(' Host OS UOA in env '+duoa+'    : '+x)
             rx=ck.access({'action':'convert_uid_to_alias', 'module_uoa':cfg['module_deps']['os'], 'uoa':setup.get('host_os_uoa','')})
             if rx['return']>0: return rx
             x=rx['string']
             ck.out(' Requested host OS UOA                  : '+x)

             ck.out('')
             rx=ck.access({'action':'convert_uid_to_alias', 'module_uoa':cfg['module_deps']['os'], 'uoa':dds.get('target_os_uoa','')})
             if rx['return']>0: return rx
             x=rx['string']
             ck.out(' Target OS UOA in env '+duoa+'  : '+x)
             rx=ck.access({'action':'convert_uid_to_alias', 'module_uoa':cfg['module_deps']['os'], 'uoa':setup.get('target_os_uoa','')})
             if rx['return']>0: return rx
             x=rx['string']
             ck.out(' Requested target OS UOA                : '+x)

             ck.out('')
             ck.out(' Target OS bits in env '+duoa+' : '+dds.get('target_os_bits',''))
             ck.out(' Requested target OS bits               : '+setup.get('target_os_bits',''))

             ck.out('')
             ck.out(' This is a possible bug - please report to the authors!')
             ck.out('')

          return {'return':33, 'error':'current host or target OS ('+str(setup)+' is not matching the one in software env '+duoa}

    # If no entries and safe mode, search packages first
    showed_warning=False

    if lx==0 and duoa=='' and tags!='' and (safe=='yes' or package_uoa!=''):
       ck.out('==========================================================================================')
       ck.out('WARNING: '+war)
       showed_warning=True

       if len(install_env)>0:
          if o=='con':
             ck.out('')
             ck.out('Reusing original and slightly pruned environment ...')
             ck.out('')

          for k in list(install_env.keys()):
              # TBD: quite ugly - maybe should record external env explicitly ...
              if k in ['LFLAGS', 'CXXFLAGS', 'CK_HOST_CPU_NUMBER_OF_PROCESSORS', 'LCORE_FLAGS']:
                 del(install_env[k])

       iii1={'out':oo,
             'package_uoa':package_uoa,
             'tags':tags,
             'or_tags':or_tags, 
             'no_tags':no_tags,
             'quiet':quiet,
             'install_to_env':iev,
             'install_env':install_env,
             'safe':safe,
             'host_os':hos,
             'target_os':tos,
             'device_id':tdid,
             'add_hint':'yes',
             'reuse_deps':reuse_deps,
             'deps_cache':deps_cache,
             'version_from':vfrom,
             'version_to':vto,
             'deps':cdeps}

       if try_to_reinstall:
          iii1['sub_deps']=i.get('current_deps',{})

       rx=internal_install_package(iii1)
       if rx['return']>0 and rx['return']!=16: return rx

       if rx['return']==0:
          duoa=rx['env_data_uoa']
          duid=rx['env_data_uid']

    # If no entries, try to detect default ones and repeat
    if lx==0 and duoa=='':
       history_deps=[]

       if o=='con' and tags!='' and not showed_warning:
          ck.out('')
          ck.out(' ********')
          ck.out(' WARNING: '+war)
          ck.out('')

          showed_warning=True

       # First, try to detect already installed software, but not registered (default)
#       FGG changed on 2017-10-20 to be able to detect new versions of soft  !
       if not (skip_default=='yes' or skip_installed.get(tplat2,'')=='yes'): # or sbov=='yes'):
          if o=='con':
             ck.out('  Trying to automatically detect required software ...')

          ii={'action':'search',
              'module_uoa':cfg['module_deps']['soft'],
              'tags':tags,
              'add_meta':'yes'}
          rx=ck.access(ii)
          if rx['return']>0: return rx

          slst=rx['lst']

          # Sorting and checking which has detection module
          detected=''
          ssi=0
          found=False
          for q in sorted(slst, key=lambda v: v.get('meta',{}).get('sort',0)):
              met=q.get('meta',{})
              auoa=q['data_uoa']
              auid=q['data_uid']
              aname=met.get('soft_name','')

              # Check no tags:
              if no_tags!='':
                 split_no_tags=no_tags.split(',')
                 soft_tags=met.get('tags',[])
                 soft_skip=False
                 for st in soft_tags:
                     if st in split_no_tags:
                        soft_skip=True
                        break
                 if soft_skip:
                    continue

              auoas.append(q['data_uoa'])
              ds=met.get('auto_detect','')
              if ds=='yes':
                 if auid not in history_deps:
                    # Check target
                    rx=ck.access({'action':'check_target',
                                  'module_uoa':cfg['module_deps']['soft'],
                                  'dict':met.get('customize',{}),
                                  'host_os_uoa':hosx,
                                  'host_os_dict':hosd,
                                  'target_os_uoa':tosx,
                                  'target_os_dict':tosd})
                    if rx['return']>0:
                       continue

                    history_deps.append(auid)
                    ssi+=1

                    if o=='con':
                       ck.out('')
                       ck.out('  '+str(ssi)+') Checking if "'+aname+'" ('+auoa+' / '+auid+') is installed ...')

                    # Detect software
                    ii={'action':'check',
                        'module_uoa':cfg['module_deps']['soft'],
                        'data_uoa':auid,
                        'skip_help':'yes',
                        'host_os':hos,
                        'target_os':tos,
                        'target_device_id':tdid,
                        'version_from':vfrom, 
                        'version_to':vto,
#                        'deps':cdeps,
                        'out':oo}
                    if len(setup)>0:
                       ii.update(setup)
                    ry=ck.access(ii)
                    if ry['return']>0:
                       if o=='con':
                          ck.out('  (warning during intermediate step: '+ry['error']+')')
                    else:
                       found=True

                       hdeps=ry.get('deps',{})
                       for hd in hdeps:
                           xhd=hdeps[hd]
                           xxhd=xhd.get('dict',{}).get('soft_uoa','')
                           if xxhd not in history_deps:
                              history_deps.append(xxhd)

          # repeat search if at least one above setup was performed
          if not found:
             if o=='con':
                ck.out('    No software auto-detection scripts found for this software in CK :( ...')

                if len(auoas)>0:
                   ck.out('')
                   ck.out('       Checked following related CK soft entries:')
                   for q in auoas:
                       ck.out('        * '+q)

          else:
             r=ck.access(iii)
             if r['return']>0: return r

             # Prune if needed
             r=prune_search_list({'lst':r['lst'], 
                                  'or_tags':or_tags, 
                                  'no_tags':no_tags,
                                  'version_from':vfrom, 
                                  'version_to':vto,
                                  'package_uoa':package_uoa})
             if r['return']>0: return r

             l=r['lst']
             lx=len(l)

    # Re-check/prune existing environment using already resolved deps
    if lx>0:
       ilx=0
       if i.get('skip_pruning_by_other_deps','')!='yes' and lx>1 and sar!='yes':
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
                         if aa.get('skip_reuse','')!='yes':

                             auoa=aa.get('uoa','')

                             # Tricky part: basically if similar and already resolved current deps are not the same is underneath ones ...
                             if auoa!='' and auoa!=juoa:
                                 skip=True
                                 break

                  if skip: break
              if not skip: nls.append(j)

          l=nls
          lx=len(l)

       # Select sub-deps (sort by version)
       if lx>1:
          ls=sorted(l, key=lambda k: (k.get('meta',{}).get('customize',{}).get('sort', 0),
                                      k.get('info',{}).get('data_name',k['data_uoa']),
                                      internal_get_val(k.get('meta',{}).get('setup',{}).get('version_split',[]), 0, 0),
                                      internal_get_val(k.get('meta',{}).get('setup',{}).get('version_split',[]), 1, 0),
                                      internal_get_val(k.get('meta',{}).get('setup',{}).get('version_split',[]), 2, 0),
                                      internal_get_val(k.get('meta',{}).get('setup',{}).get('version_split',[]), 3, 0),
                                      internal_get_val(k.get('meta',{}).get('setup',{}).get('version_split',[]), 4, 0)),
                    reverse=True)

          l=ls

          if ran=='yes':
             from random import randint
             ilx=randint(0, lx-1)
          elif quiet=='yes':
             ilx=0
          else:
             if o=='con':
                xq='required software'
                if name!='': xq='"'+name+'"'

                xq+=' with tags="'+tags+'"'

                if len(setup)>0:
                   import json

                   ro=readable_os({'setup':setup})
                   if ro['return']>0: return ro
                   setup1=ro['setup1']

                   xq+=' and setup='+json.dumps(setup1)

                ck.out('')
                ck.out('More than one environment found for '+xq+':')
                zz={}
                for z in range(0, lx):
                    j=l[z]

                    zi=j.get('info',{})
                    zm=j.get('meta',{})
                    zu=j.get('data_uid','')
                    zdn=zi.get('data_name','')
                    cus=zm.get('customize',{})
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
                           if juoa!='': # if empty, it most likely means that this unresolved dependency
                                        # is for a different target
                              jtags=jj.get('tags','')
                              jver=jj.get('ver','')

                              js='                                  '
                              js+='- Depends on "'+j+'" (env UOA='+juoa+', tags="'+jtags+'", version='+jver+')'
                              ck.out(js)

                ck.out('')
                rx=ck.inp({'text':'Select one of the options for '+xq+' or press Enter for 0: '})
                x=rx['string'].strip()

                if x=='': x='0'

                if x not in zz:
                   return {'return':1, 'error':'option is not recognized'}

                ilx=int(x)

       if ilx<len(l):
          duid=l[ilx]['data_uid']
          duoa=duid

          dname=l[ilx].get('info',{}).get('data_name','')

          dd=l[ilx].get('meta',{})

          if o=='con' and i.get('print','')=='yes':
             x=duoa
             if duid!=duoa: x+=' ('+duid+')'
             ck.out('CK environment found using tags "'+tags+'" : '+x)

    # No registered environments found and environment UOA is not explicitly defined
    if duoa=='':
       if tags!='':
          if not showed_warning:
             ck.out('==========================================================================================')
             ck.out('WARNING: '+war)

          rx=internal_install_package({'out':oo,
                                       'tags':tags,
                                       'or_tags':or_tags, 
                                       'no_tags':no_tags,
                                       'quiet':quiet,
                                       'install_to_env':iev,
                                       'install_env':install_env,
                                       'safe':safe,
                                       'host_os':hos,
                                       'target_os':tos,
                                       'device_id':tdid,
                                       'reuse_deps':reuse_deps,
                                       'deps_cache':deps_cache,
                                       'version_from':vfrom,
                                       'version_to':vto,
                                       'deps':cdeps})
          if rx['return']>0: return rx

          duoa=rx['env_data_uoa']
          duid=rx['env_data_uid']

       if duoa=='':
          if o=='con':
             ck.out('    CK packages are not found for this software :( !')
             ck.out('')

             if len(auoas)>0:
                if len(auoas)==1:
                   rx=ck.access({'action':'print_help',
                                 'module_uoa':cfg['module_deps']['soft'],
                                 'data_uoa':auoas[0],
                                 'platform':hplat})

                   rx=ck.inp({'text':'       Would you like to manually register software, i.e. if it is in an unusual path (y/N): '})
                   x=rx['string'].strip().lower()
                   if x=='yes' or x=='yes':
                      ck.out('')
                      rx=ck.access({'action':'setup',
                                    'module_uoa':cfg['module_deps']['soft'],
                                    'data_uoa':auoas[0],
                                    'out':'con'})
                      if rx['return']>0: return rx
                      ck.out('')

                else:
                   # Show possible Wiki page
                   rx=ck.inp({'text':'       Would you like to open wiki pages about related software (with possible installation info) (y/N): '})
                   x=rx['string'].strip().lower()

                   if x=='yes' or x=='yes':
                      ck.out('')
                      for q in auoas:
                          rx=ck.access({'action':'wiki',
                                        'module_uoa':cfg['module_deps']['soft'],
                                        'data_uoa':q})
                          if rx['return']>0: return rx
                      ck.out('')


          if o=='con':
             ck.out('')
          return {'return':1, 'error':war}

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

    dname=r.get('data_name','')
    if dname!='':
        d['data_name']=dname

    suoa=d.get('soft_uoa','')
    cs=None
    if suoa!='':
       r=ck.access({'action':'load',
                    'module_uoa':cfg['module_deps']['soft'],
                    'data_uoa':suoa})
       if r['return']>0: return r

       salias=r['data_alias']
       d['soft_alias']=salias

       # Check if has custom script
       rx=ck.load_module_from_path({'path':r['path'], 'module_code_name':cfg['custom_script_name'], 'skip_init':'yes'})
       if rx['return']==0: 
          cs=rx['code']

    # Check that all sub dependencies still exists (if full path)
    outdated=False
    to_delete=False
    err=''

    edeps=d.get('deps',{}) # sub-dependencies of the selected environment 
                           # (normally already resolved, but check if software changed in the mean time)
    for q in edeps:
        qq=edeps[q]
        cqq=qq.get('dict',{}).get('customize',{})
        sfc=cqq.get('skip_file_check','')
        fp=cqq.get('full_path','')

        if sfc!='yes' and fp!='' and not os.path.isfile(fp):
           outdated=True
           err='one of sub-dependencies ('+q+') have changed (file '+fp+' not found)'
           break

        deuoa=qq.get('uoa','')
        if deuoa!='':
           rx=ck.access({'action':'find',
                         'module_uoa':work['self_module_uid'],
                         'data_uoa':deuoa})
           if rx['return']>0:
              if rx['return']!=16: return rx
              outdated=True
              err='one of sub-dependencies ('+q+') have changed (CK environment '+deuoa+' not found)'
              break

        if reuse_deps=='yes' and skip_cache!='yes':
           # Check in cache!
           dmatch2={'setup':setup, 'tags':qq.get('tags','').split(',')}
           dc_found=False
           for dc_q in deps_cache:
               d1=dc_q.get('meta',{})
               r=ck.compare_dicts({'dict1':d1, 'dict2':dmatch2})
               if r['return']>0: return r
               if r['equal']=='yes':
                  dc_found=True
                  break

           if not dc_found:
              deps_cache.append({'meta':dmatch2, 'uoa':deuoa})

    # Check if has changed but try to continue
    if outdated and ' have changed ' in err and o=='con' and quiet!='yes':
       ck.out('')
       ck.out('    WARNING: '+err)

       ck.out('')
       rx=ck.inp({'text':'    Would you like to continue at your own risk (y/N): '})
       x=rx['string'].strip().lower()

       if x=='y' or x=='yes':
          outdated=False

    # Check if file exists for current dependency
    verx=''
    cus=d.get('customize',{})
    fp=cus.get('full_path','')

    tc='it appears that your environment has changed - '
    if not outdated and fp!='' and cus.get('skip_file_check','')!='yes' and not os.path.isfile(fp):
       err=tc+'software file not found in a specified path ('+fp+')'
       outdated=True

    ver_in_env=cus.get('version','') # detected version during installation
    if not outdated and ver_in_env!='':
       scmd=cus.get('soft_version_cmd',{}).get(ck_os_name,'')
       if cus.get('skip_version_recheck','')!='yes' and scmd!='' and 'parse_version' in dir(cs):
          # Check version (via customized script) ...
          ii={'action':'get_version',
              'module_uoa':cfg['module_deps']['soft'],
              'full_path':fp,
              'bat':'',
              'host_os_dict':hosd,
              'target_os_dict':tosd,
              'cmd':scmd,
              'custom_script_obj':cs,
              'use_locale':cus.get('use_locale_for_version','')}
          rx=ck.access(ii)
          if rx['return']==0:
             verx=rx['version']
             if verx!='' and verx!=ver_in_env:
                err=tc+'version during installation ('+ver_in_env+') is not the same as current version ('+verx+')'
                outdated=True

    if outdated:
       if o=='con':
          ck.out('')
          ck.out('WARNING: '+err)

          ck.out('')
          rx=ck.inp({'text':'Would you like to remove outdated environment entry from CK (Y/n)? '})
          x=rx['string'].strip()

          if x=='n' or x=='no':
             return {'return':1, 'error':err}
          to_delete=True

       # Deleting outdated environment
       if to_delete:
          if o=='con':
             ck.out('')
             ck.out('Removing outdated environment entry '+duoa+' ...')

          rx=ck.access({'action':'delete',
                        'module_uoa':work['self_module_uid'],
                        'data_uoa':duoa})
          if rx['return']>0: return rx

          return {'return':1, 'error':'Outdated environment was removed - please, try again!'}

    # Update cache
    if reuse_deps=='yes' and skip_cache!='yes':
       deps_cache.append({'meta':dmatch, 'uoa':duoa})

    # Prepare environment and bat
    env=i.get('env',{})
    xenv=d.get('env',{})
    env.update(xenv)

    env_call=hosd.get('env_call','')
    bin_prefix=hosd.get('bin_prefix','')

    # Process CMD first:
    sb=''

    es=d.get('env_script','')
    ppu=''
    if i.get('force_env_init','')=='yes':
       ppu=' 1'

    if es!='':
       pp=os.path.join(p,es)
       if i.get('key','')!='':
          sb+=eset+' CK_ENV_SCRIPT_'+i['key'].upper()+'='+pp+'\n'
       sb+=env_call+' '+pp+ppu+'\n'

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

    return {'return':0, 'env_uoa':duoa, 'env':env, 'bat':sb, 'lst':l, 'dict':d, 'detected_version':verx}

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

        if len(meta)==0:
           continue

        cus=meta.get('customize',{})
        setup=meta.get('setup',{})
        tags=meta.get('tags',[])

        host_os_uoa=setup.get('host_os_uoa','')
        target_os_uoa=setup.get('target_os_uoa','')
        tbits=setup.get('target_os_bits','')
        version=cus.get('version','')
        sversion=setup.get('version_split',[])

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
           vv['version_split']=sversion
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

    # Sort by target_os_uoa, name and split version
    vs=sorted(view, key=lambda k: (k['target_os_uoa'],
                                   k['tbits'],
                                   k['data_name'],
                                   internal_get_val(k.get('version_split',[]), 0, 0),
                                   internal_get_val(k.get('version_split',[]), 1, 0),
                                   internal_get_val(k.get('version_split',[]), 2, 0),
                                   internal_get_val(k.get('version_split',[]), 3, 0),
                                   internal_get_val(k.get('version_split',[]), 4, 0)),
              reverse=True)

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
                  or
              (device_id)

              (repo_uoa)             - repo where to limit search

              deps                   - dependencies dict

              (reuse_deps)           - if 'yes' reuse all deps if found in cache by tags
              (deps_cache)           - list with resolved deps

              (env)                  - env

              (install_env)          - env during installation

              (add_customize)        - if 'yes', add to deps customize field from the environment 
                                       (useful for program compilation)

              (skip_dict)            - if 'yes', do not add to deps dict field from the environment 
                                       (useful for program compilation)

              (skip_auto_resolution) - if 'yes', do not check if deps are already resolved

              (random)               - if 'yes' and there is a choice, select random
                                       (useful for quiet experiment crowdsourcing such as sw/hw crowdtuning)

              (quiet)                - if 'yes', automatically provide default answer to all questions when resolving dependencies ... 

              (install_to_env)       - install dependencies to env instead of CK-TOOLS (to keep it clean)!

              (safe)                 - safe mode when searching packages first instead of detecting already installed soft
                                       (to have more deterministic build)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - string for bat file calling all bats ...
              cut_bat      - string for bat file calling all bats (does not include deps that are explicitly excluded) ...
              deps         - updated deps (with uoa)
              env          - updated env
            }

    """

    import copy

    o=i.get('out','')

    if o=='con':
       ck.out('')
       ck.out('  -----------------------------------')
       ck.out('  Resolving software dependencies ...')

    sb=''
    sb1=''

    install_env=i.get('install_env',{})

    sar=i.get('skip_auto_resolution','')

    deps=i.get('deps',{})

    deps_cache=i.get('deps_cache',[])
    reuse_deps=i.get('reuse_deps','')

    ran=i.get('random','')
    quiet=i.get('quiet','')

    iev=i.get('install_to_env','')
    safe=i.get('safe','')

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')
    if tdid=='': tdid=i.get('device_id','')

    user_env=False
    if hos!='' or tos!='' or tdid!='': user_env=True

    # Get some info about OS
    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.os'],
        'host_os':hos,
        'target_os':tos,
        'device_id':tdid,
        'skip_info_collection':'yes'}
    r=ck.access(ii)
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    hplat=hosd.get('ck_name','')
    hplat2=hosd.get('ck_name2','')
    tplat=tosd.get('ck_name','')
    tplat2=tosd.get('ck_name2','')

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

    remote=tosd.get('remote','')

    tbits=tosd.get('bits','')

    # Checking deps
    env=i.get('env',{})
    enruoa=i.get('repo_uoa','')

    ac=i.get('add_customize','')
    sd=i.get('skip_dict','')

    res=[]
    iv=0

    sdeps=sorted(deps, key=lambda v: deps[v].get('sort',0))

    xsb=''  # Append to the end
    xsb1='' # Append to the end

    for k in sdeps:
        q=deps[k]

        if q.get('skipped','')=='yes':
           continue

        if q.get('enabled','')!='yes':
           check_env=q.get('enable_if_env',{})
           if len(check_env)>0:
              enable=True
              for j in check_env:
                  v=check_env[j]
                  if install_env.get(j,'').lower()!=v.lower():
                     enable=False
                     break

              if enable:
                 q['enabled']='yes'
              else:
                 q['skipped']='yes'
                 continue

        if q.get('skipped','')!='yes':
           check_env=q.get('disable_if_env',{})
           if len(check_env)>0:
              disable=True
              for j in check_env:
                  v=check_env[j]
                  if install_env.get(j,'').lower()!=v.lower():
                     disable=False
                     break

              if disable:
                 q['skipped']='yes'
                 continue
              else:
                 q['enabled']='yes'

        ytos=tos
        ytdid=tdid
        ytosx=tosx
        ytosd=tosd

        tags=q.get('tags','')
        or_tags=q.get('or_tags','')
        no_tags=q.get('no_tags','')
        name=q.get('name','')
        local=q.get('local','')
        sd=q.get('skip_default','')
        sinst=q.get('skip_installed',{})

        vfrom=q.get('version_from',[])
        vto=q.get('version_to',[])

        ek=q.get('env_key','')

        uoa=q.get('uoa','')

        skip_cache=q.get('skip_cache','')

        # Check if restricts dependency to a given host or target OS
        rx=ck.access({'action':'check_target',
                      'module_uoa':cfg['module_deps']['soft'],
                      'dict':q,
                      'host_os_uoa':hosx,
                      'host_os_dict':hosd,
                      'target_os_uoa':ytosx,
                      'target_os_dict':ytosd})
        if rx['return']>0:
           continue

        if q.get('force_target_as_host','')=='yes':
            ytos=hos
            ytdid=''
            ytosx=hosx
            ytosd=hosd

        # Updating tags if needed based on host/target
        xtags=[]
        tx=q.get('update_tags_by_host_platform',{}).get(hplat,'')
        if tx!='': xtags.append(tx)
        tx=q.get('update_tags_by_host_platform2',{}).get(hplat2,'')
        if tx!='': xtags.append(tx)
        tx=q.get('update_tags_by_target_platform',{}).get(tplat,'')
        if tx!='': xtags.append(tx)
        tx=q.get('update_tags_by_target_platform2',{}).get(tplat2,'')
        if tx!='': xtags.append(tx)
        tx=q.get('update_tags_by_target_os_uoa',{}).get(ytosx,'')       # Ugly, but quick
        if tx!='': xtags.append(tx)

        for tx in xtags:
            if tags!='': tags+=','
            tags+=tx.strip()

        # Check if has associated package (in case of rebuilding deps for replay)
        qdict=q.get('dict',{})
        package_uoa=q.get('package_uoa','')
        if package_uoa=='':
           package_uoa=qdict.get('package_uoa','')
        if package_uoa=='':
           package_uoa=qdict.get('customize',{}).get('used_package_uid','')

        xinstall_env=copy.deepcopy(qdict.get('customize',{}).get('install_env',{}))
#        xinstall_env.update(install_env)
#       install_env=copy.deepcopy(xinstall_env) # This is bug - install_env is a global env which is common for the first package!

        # Try to set environment
        iv+=1

        if o=='con':
           x='*** Dependency '+str(iv)+' = '+k
           if name!='': x+=' ('+name+')'
           x+=':'
           ck.out('')
           ck.out(x)

        ii={'host_os':hos,
            'original_target_os_name2':tplat2,
            'target_os':ytos,
            'target_device_id':ytdid,
            'tags':tags,
            'or_tags':or_tags,
            'no_tags':no_tags,
            'repo_uoa':enruoa,
            'env':env,
            'uoa':uoa,
            'deps':deps,
            'current_deps':qdict.get('deps',{}),
            'deps_cache':deps_cache,
            'reuse_deps':reuse_deps,
            'skip_cache':skip_cache,
            'skip_auto_resolution':sar,
            'skip_default':sd,
            'skip_installed':sinst,
            'local':local,
            'random':ran,
            'name':name,
            'key':ek,
            'skip_pruning_by_other_deps':q.get('skip_pruning_by_other_deps',''),
            'quiet':quiet,
            'force_env_init':q.get('force_env_init',''),
            'install_to_env':iev,
            'install_env':xinstall_env,
            'version_from':vfrom,
            'version_to':vto,
            'package_uoa':package_uoa,
            'safe':safe
           }

        if o=='con': ii['out']='con'

        rx=set(ii)
        if rx['return']>0: return rx

        lst=rx['lst']
        dd=rx['dict']

        package_uoa=dd.get('package_uoa','')
        if package_uoa=='':
           package_uoa=dd.get('customize',{}).get('used_package_uid','')
        if package_uoa!='':
           q['package_uoa']=package_uoa # to be able to rebuild env for replay on another machine

        dver=rx.get('detected_version','')
        if dver!='': q['detected_ver']=dver

        # add choices
        zchoices=[]
        for zw in lst:
            zchoices.append(zw['data_uid'])

        if 'choices' not in q or len('choices')==0: 
           q['choices']=zchoices

        cus=dd.get('customize',{})

        if ac=='yes': q['cus']=cus
        if sd!='yes' or q.get('add_dict','')=='yes': q['dict']=dd

        ver=cus.get('version','')
        if ver!='': q['ver']=ver

        uoa=rx['env_uoa']
        q['uoa']=uoa
        q['num_entries']=len(lst)

        if o=='con':
           ck.out('')
           x='    Resolved. CK environment UID = '+uoa
           if dver!='': 
              x+=' (detected version '+dver+')'
           elif ver!='':
              x+=' (version '+ver+')'
           ck.out(x)

        bdn=cus.get('build_dir_name','')
        if bdn!='': q['build_dir_name']=bdn # Needed to suggest directory name for building libs

        if uoa not in res: res.append(uoa)

        env=rx['env']

        bt=rx['bat']

        q['bat']=bt
        sb+=bt

        if q.get('skip_from_bat','')!='yes':
           sb1+=bt

    if o=='con':
       ck.out('  -----------------------------------')

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

        if 'tmp' in tags:
           continue

        sftags=''
        for t in tags:
            if t!='':
               if sftags!='': sftags+=','
               sftags+=t

        host_os_uoa=setup.get('host_os_uoa','')
        target_os_uoa=setup.get('target_os_uoa','')
        tbits=setup.get('target_os_bits','')
        version=setup.get('version','')

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

              rx=ck.inp({'text':'  Select one of the options for soft UOA: '})
              x=rx['string'].strip()

              if x not in num:
                 return {'return':1, 'error':'option is not recognized'}

              soft_uoa=num[x]

           meta['soft_uoa']=soft_uoa

           # Update environment entry
           rx=ck.access({'action':'update',
                         'module_uoa':work['self_module_uid'],
                         'data_uoa':duoa,
                         'data_name':dname,
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
            'tags':sftags,
            'package_uoa':package_uoa,
            'skip_device_info_collection':'yes',
            'soft_name':dname,
            'env':penv,
            'env_data_uoa':duid}
        if i.get('reset_env','')!='': ii['reset_env']=i['reset_env']
        rx=ck.access(ii)
        if rx['return']>0: 
           rrx=rx['return']
           if rrx!=32 and rrx!=33:
              return rx
           if o=='con':
              if rrx==32:
                 ck.out('')
                 ck.out('One of the dependencies is missing for this CK environment!')
              elif rrx==33:
                 ck.out('')
                 ck.out('This environment has either missing dependencies or strange mismatch between registered software environment and current setup!')

              ck.out('')
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

##############################################################################
# internal function: get value from list without error if out of bounds

def internal_get_val(lst, index, default_value):
    v=default_value
    if index<len(lst):
       v=lst[index]
    return v

##############################################################################
# Prune search list by no_tags

def prune_search_list(i):
    """
    Input:  {
              lst                    - list of entries after 'search'
              (or_tags)              - add entries which has groups of tags separated by ;
              (no_tags)              - string of tags to exclude
              (version_from)         - check version starting from ... (list of numbers)
              (version_to)           - check version up to ... (list of numbers)
              (package_uoa)          - prune by specific package 
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              lst          - pruned list

              (skipped_because_of_version) - if 'yes', skip because of version check
            }
    """

    lst=i.get('lst',[])

    package_uoa=i.get('package_uoa','')

    no_tags=i.get('no_tags','')
    ntags=[]
    if no_tags!='': ntags=no_tags.split(',')

    or_tags=i.get('or_tags','')
    otags=[]
    if or_tags!='': 
       xotags=or_tags.split(';')
       for q in xotags:
           otags.append(q.split(','))

    vfrom=i.get('version_from',[])
    vto=i.get('version_to',[])

    nlst=[]

    skipped_because_of_version=''

    for q in lst:
        meta=q.get('meta','')
        tags=meta.get('tags',[])

        skip=False

        # Check package UOA
        if package_uoa!='':
           xpackage_uoa=meta.get('package_uoa','')
           if xpackage_uoa=='':
              xpackage_uoa=meta.get('customize',{}).get('used_package_uid','')
           if xpackage_uoa!='' and xpackage_uoa!=package_uoa:
              skip=True

        # Check that not temporal entry (unfinished installation)
        if not skip and 'tmp' in tags:
           skip=True

        # Check or tags
        if not skip and len(otags)>0:
           found=False
           for t in otags:
               found=True
               for t1 in t:
                   if t1 not in tags:
                      found=False
                      break
               if found:
                  break
           if not found:
              skip=True

        # Check no tags
        if not skip:
           for t in ntags:
               if t in tags:
                   skip=True
                   break

        # Check version
        if not skip and (len(vfrom)>0 or len(vto)>0):
           v=meta.get('setup',{}).get('version_split',[])

           # first check from env, but if not set, check from package
           if len(v)==0:
              v=meta.get('customize',{}).get('version_split',[])
              if len(v)==0:
                 ver=meta.get('customize',{}).get('version','')
 
                 if ver!='':
                    rx=ck.access({'action':'split_version',
                                  'module_uoa':cfg['module_deps']['soft'],
                                  'version':ver})
                    if rx['return']>0: return rx
                    v=rx['version_split']

           if len(vfrom)>0:
              r=ck.access({'action':'compare_versions',
                           'module_uoa':cfg['module_deps']['soft'],
                           'version1':vfrom,
                           'version2':v})
              if r['return']>0: return r
              result=r['result']

              if result=='>':
                 skip=True
                 skipped_because_of_version='yes'

           if not skip and len(vto)>0:
              r=ck.access({'action':'compare_versions',
                           'module_uoa':cfg['module_deps']['soft'],
                           'version1':v,
                           'version2':vto})
              if r['return']>0: return r
              result=r['result']

              if result=='>':
                 skip=True
                 skipped_because_of_version='yes'

        if not skip:
            nlst.append(q)

    return {'return':0, 'lst':nlst, 'skipped_because_of_version':skipped_because_of_version}

##############################################################################
# remote env entry and installed package

def clean(i):
    """
    Input:  {
              (data_uoa) - entries to be cleaned (wildcards can be used)
              (repo_uoa)
              (tags)
              (force)    - if 'yes', force delete
              (f)        - if 'yes', force delete
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import copy
    import os
    import shutil

    oo=''
    o=i.get('out','')
    if o=='con': oo=o

    force=i.get('force','')
    if force=='': force=i.get('f','')

    ii=copy.deepcopy(i)
    ii['action']='show'
    ii['out']=''

    r=ck.access(ii)
    if r['return']>0: return r

    lst=r['lst']

    # Check default path
    r=ck.access({'action':'prepare_install_path',
                 'module_uoa':cfg['module_deps']['package']})
    if r['return']>0: return r

    path=r['path']

    for q in lst:
        ruid=q['repo_uid']
        duid=q['data_uid']
        duoa=q['data_uoa']

        d=q['meta']
        info_data_name  = q.get('info',{}).get('data_name','UNKNOWN')
        tags_csv        = ','.join(d.get('tags',[]))

        cus=d.get('customize',{})
        fp=cus.get('full_path','')
        fp4=''

        if fp.startswith(path):
           j=1
           if path.endswith(os.path.sep) or path.endswith('/'):
              j=0
           fp1=fp[len(path)+j:]

           fp2=fp1.split(os.path.sep)

           if len(fp2)>0:
              fp3=fp2[0]

              if fp3!='':
                 fp4=os.path.join(path,fp3)

        x=''
        if fp4!='' and os.path.isdir(fp4):
           x=' package in dir "'+fp4+'" and'

        s=''
        if force=='yes':
           s='yes'
        elif o=='con':
           r=ck.inp({'text':'Are you sure to delete'+x+' CK entry env:"'+duoa+'" - a '+info_data_name+' with tags: '+tags_csv+' (y/N): '})
           if r['return']>0: return r
           s=r['string'].strip().lower()
           if s=='y': s='yes'

        if s=='yes':
           # Delete entry
           r=ck.access({'action':'rm',
                        'module_uoa':work['self_module_uid'],
                        'data_uoa':duid,
                        'repo_uoa':ruid,
                        'force':s,
                        'out':oo})
           if r['return']>0: return r

           # Delete package
           if fp4!='' and os.path.isdir(fp4):
              shutil.rmtree(fp4)

    return {'return':0}

##############################################################################
# internal function to install package

def internal_install_package(i):
    """
    Input:  {
              (host_os)              - host OS (detect, if ommitted)
              (target_os)            - target OS (detect, if ommitted)
              (target_device_id)     - target device ID (detect, if omitted)
                     or
              (device_id)

              (package_uoa)          - fix package (useful for replay ...)
              (tags)                 - search UOA by tags (separated by comma)
              (or_tags)              - add entries which has groups of tags separated by ;
              (no_tags)              - exclude entris with these tags separated by comma

              (deps)                 - already resolved deps
              (sub_deps)             - deps for the package to be installed (for replay mainly)

              (reuse_deps)           - if 'yes' reuse all deps if found in cache by tags
              (deps_cache)           - list with resolved deps

              (quiet)                - if 'yes', automatically provide default answer to all questions when resolving dependencies ... 

              (install_to_env)       - install dependencies to env instead of CK-TOOLS (to keep it clean)!

              (install_env)          - customize installation (useful for replay to rebuild proper package with external env)

              (safe)                 - safe mode when searching packages first instead of detecting already installed soft
                                       (to have more deterministic build)

              (version_from)         - check version starting from ... (list of numbers)
              (version_to)           - check version up to ... (list of numbers)

              (add_hint)             - if 'yes', can skip package installation
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              env_data_uoa - installed package data UOA (can be "" if not found)
              env_data_uid - installed package data UID (can be "" if not found)
            }

    """

    import os

    o=i.get('out','')
    oo=''
    if o=='con': oo=o

    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('device_id','')
    package_uoa=i.get('package_uoa','')

    deps_cache=i.get('deps_cache',[])
    reuse_deps=i.get('reuse_deps','')

    tags=i.get('tags','')
    or_tags=i.get('or_tags','')
    no_tags=i.get('no_tags','')
    quiet=i.get('quiet','')
    iev=i.get('install_to_env','')
    install_env=i.get('install_env',{})
    safe=i.get('safe','')
    ah=i.get('add_hint','')

    vfrom=i.get('version_from',[])
    vto=i.get('version_to',[])

    cdeps=i.get('deps',{})

    # Next, try to install via package for a given software
    if o=='con':
       ck.out('')
       ck.out('  Searching and installing CK software packages ...')
       if package_uoa!='':
          # Try to detect alias
          rx=ck.access({'action':'load',
                        'module_uoa':cfg['module_deps']['package'],
                        'data_uoa':package_uoa})
          if rx['return']>0: return rx
          package_uid=rx['data_uid']
          package_alias=rx['data_alias']

          ck.out('    * package UOA: '+package_alias+' ('+package_uid+')')
       ck.out('    * tags:        '+tags)
       ck.out('    * or tags:     '+or_tags)
       ck.out('    * no tags:     '+no_tags)
       ck.out('')

#          if quiet=='yes':
#             ck.out('  Searching and installing package with these tags automatically ...')
#             a='y'
#          else:
#             rx=ck.inp({'text':'  Would you like to search and install package with these tags automatically (Y/n)? '})
#             a=rx['string'].strip().lower()
#
#          if a!='n' and a!='no':
    try:
         save_cur_dir=os.getcwd()
    except OSError:
        os.chdir('..')
        save_cur_dir=os.getcwd()

    vv={'action':'install',
        'module_uoa':cfg['module_deps']['package'],
        'data_uoa':package_uoa,
        'out':oo,
        'tags':tags,
        'or_tags':or_tags,
        'no_tags':no_tags,
        'install_to_env':iev,
        'env':install_env,
        'safe':safe,
        'host_os':hos,
        'target_os':tos,
        'device_id':tdid,
        'reuse_deps':reuse_deps,
        'deps_cache':deps_cache,
        'version_from':vfrom,
        'version_to':vto,
        'add_hint':ah}

    # Check if there is a compiler in resolved deps to reuse it
    xdeps=i.get('sub_deps',{})
    if cdeps.get('compiler',{}).get('uoa','')!='': xdeps['compiler']=cdeps['compiler']
    if cdeps.get('compiler-mcl',{}).get('uoa','')!='': xdeps['compiler-mcl']=cdeps['compiler-mcl']
    if len(xdeps)>0: vv['deps']=xdeps

    duoa=''
    duid=''

    rx=ck.access(vv)
    if rx['return']==0:
       duoa=rx['env_data_uoa']
       duid=rx['env_data_uid']

       os.chdir(save_cur_dir)
    elif rx['return']!=16:
       return rx

    return {'return':0, 'env_data_uoa':duoa, 'env_data_uid':duid}

##############################################################################
# set env for command line (pre-set various flags)

def xset(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    # Generate tmp file
    i['local']='yes'
    i['bat_file']='tmp-ck-env.bat'
    i['bat_new']='yes'
    i['print']='yes'

    return set(i)

##############################################################################
# pre-load environment for the shell

def virtual(i):
    """
    Input:  {
              data_uoa or uoa   - environment UOA to pre-load (see "ck show env") - can be listed via ,

              (shell_cmd)       - command line to run in the "environment-enriched" shell (make sure it is suitably quoted)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    duoa        = i.get('data_uoa', i.get('uoa','') )

    if duoa.find(',')!=-1:      # TODO: becomes deprecated (but still works) in 1.10, becomes an error in 1.11
        # ck.out('')
        # ck.out('DEPRECATED: You seem to be using CSV format within a CID. Please list multiple CIDs on your command line instead.')
        # ck.out('')
        list_of_uoa = duoa.split(',')
    else:
        list_of_uoa = [ duoa ]

    for xcid in i.get('xcids',[]):
        if xcid['module_uoa'] == 'env':
            list_of_uoa.append( xcid['data_uoa'] )
        else:
            return {'return':1, 'error':"all CID entries have to be of 'env' type"}

    shell_script_contents_for_unix      = '' # string with env
    shell_script_contents_for_windows   = '' # string with env

    for uoa in list_of_uoa:
        i['uoa']=uoa

        r=set(i)
        if r['return']>0: return r

        shell_script_contents_for_unix +='\n'+r['bat']+'\n'

        if shell_script_contents_for_windows != '': shell_script_contents_for_windows+=' & '
        shell_script_contents_for_windows += r['bat'].replace('\n','')

    # Run shell
    import platform
    import os
    import subprocess

    shell_cmd        = i.get('shell_cmd', None)

    ck.out('')
    ck.out('Warning: you are in a new shell with a pre-set CK environment. Enter "exit" to return to the original one!')

    if platform.system().lower().startswith('win'): # pragma: no cover
        if shell_cmd:
            shell_script_contents_for_windows += ' & ' + shell_cmd
            termination_flag = '/C'     # terminate the CMD shell when the environment script & shell_cmd are over
        else:
            termination_flag = '/K'     # remain in the CMD shell

        p = subprocess.Popen(['cmd', termination_flag, shell_script_contents_for_windows], shell = True, env=os.environ)
        p.wait()
        return_code  = p.returncode
    else:
        rx=ck.gen_tmp_file({})
        if rx['return']>0: return rx
        file_name=rx['file_name']

        rx=ck.save_text_file({'text_file':file_name, 'string':shell_script_contents_for_unix })
        if rx['return']>0: return rx

        full_cmd_list    = ['/bin/bash','--rcfile', file_name, '-i'] + ( ['-c', shell_cmd] if shell_cmd else [] )

        return_code = subprocess.call(full_cmd_list, shell = False)

    return {'return':return_code, 'error':'Unknown error from the nested shell'}


##############################################################################
# show the shell script for setting up this env

def view(i):
    """
    Input:  {
              data_uoa or uoa   - environment UOA to pre-load (see "ck virtual env")
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    duoa        = i.get('data_uoa', i.get('uoa', '*') )
    tags_csv    = i.get('tags')

    if duoa.find(',')!=-1:      # TODO: becomes deprecated (but still works) in 1.10, becomes an error in 1.11
        # ck.out('')
        # ck.out('DEPRECATED: You seem to be using CSV format within a CID. Please list multiple CIDs on your command line instead.')
        # ck.out('')
        list_of_uoa = duoa.split(',')
    elif duoa.find('*')!=-1 or duoa.find('?')!=-1 or tags_csv:
        searched_adict = ck.access( dict(i, action='search') )
        if searched_adict['return']>0: return rx

        list_of_uoa = [ entry['data_uoa'] for entry in searched_adict['lst'] ]
    else:
        list_of_uoa = [ duoa ]

    for xcid in i.get('xcids',[]):
        if xcid['module_uoa'] == 'env':
            list_of_uoa.append( xcid['data_uoa'] )
        else:
            return {'return':1, 'error':"all CID entries have to be of 'env' type"}

    for uoa in list_of_uoa:

        loaded_adict = ck.access({'action':'load',
            'module_uoa':   'env',
            'data_uoa':     uoa,
        })
        if loaded_adict['return']>0: return loaded_adict

        env_script_name     = loaded_adict['dict']['env_script']
        setup_script_path   = os.path.join( loaded_adict['path'], env_script_name)
        rem_marker          = ('#' if env_script_name=='env.sh' else 'REM')
        header_line         = '{} {}[ {} ]{}'.format(rem_marker, '-' * 40, setup_script_path, '-' * 40)

        ck.out( header_line )

        with open(setup_script_path, 'r') as setup_script_file:
            for line in setup_script_file:
                ck.out( line.rstrip() )
        ck.out( "\n\n" )

    return {'return':0}

##############################################################################
# remove tmp entries (when installation to env entry failed)

def rmtmp(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    i['action']='rm'
    i['data_uoa']='*'

    tags=i.get('tags','')
    if tags!='': tags+=','
    tags+='tmp'

    i['tags']=tags

    return ck.access(i)

##############################################################################
# get all versions from deps (recursively)

def get_all_versions_in_deps(i):
    """
    Input:  {
              deps        - deps dict
              (key)       - current key
              (only_root) - if 'yes', check only root keys

              (versions)  - current versions
              (tag_versions) - current versions by tags
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              versions     - all versions for all deps
              tag_versions     - all versions for all deps by tags
            }

    """

    deps=i['deps']
    key=i.get('key','')

    versions=i.get('versions',{})
    tversions=i.get('tversions',[])

    only_root=(i.get('only_root','')=='yes')

    for k in deps:
        xkey=key
        if xkey!='': xkey+='#'
        xkey+=k

        d=deps[k]

        dd=d.get('dict',{})

        tags=dd.get('tags',[])
        stags=','.join(tags)

        ver=d.get('ver','')

        versions[xkey]=ver

        if stags not in tversions:
           tversions.append(stags)

        deps2=dd.get('deps',{})
        if not only_root and len(deps2)>0:
           r=get_all_versions_in_deps({'deps':deps2, 'key':xkey, 'versions':versions, 'tag_versions':tversions})
           if r['return']>0: return r

    return {'return':0, 'versions':versions, 'tag_versions':tversions}

##############################################################################
# extracting summary of all deps

def deps_summary(i):
    """
    Input:  {
              deps - resolved deps
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              deps_summary - summary of deps
            }

    """

    deps=i['deps']
    ds=i.get('deps_summary',{})

    for x in deps:
        d=deps[x]
        dd=d.get('dict',{})

        ds[x]={}

        cx=dd.get('customize',{})

        ds[x]['tags']=d.get('tags',[])
        ds[x]['name']=d.get('name','')

        ds[x]['package_tags']=','.join(dd.get('tags',[]))
        ds[x]['data_name']=dd.get('data_name','')

        puoa=dd.get('package_uoa','')
        if puoa=='':
           puoa=d.get('cus',{}).get('used_package_uid','')
        ds[x]['package_uoa']=puoa

        ds[x]['version']=cx.get('version','')
        ds[x]['git_revision']=cx.get('git_info',{}).get('revision','')
        ds[x]['git_iso_datetime_cut_revision']=cx.get('git_info',{}).get('iso_datetime_cut_revision','')

        sdeps=dd.get('deps',{})
        if len(sdeps)>0:
           # Recursion
           r=deps_summary({'deps':sdeps})
           if r['return']>0: return r
           ds[x]['deps']=r['deps_summary']

    return {'return':0, 'deps_summary':ds}
