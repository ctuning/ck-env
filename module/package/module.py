#
# Collective Knowledge (package)
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
fix_env_for_rebuild={"PACKAGE_GIT": "NO", 
                     "PACKAGE_WGET": "NO",
                     "PACKAGE_PATCH": "NO",
                     "PACKAGE_PATCH": "NO",
                     "PACKAGE_UNGZIP": "NO",
                     "PACKAGE_UNTAR": "NO",
                     "PACKAGE_UNBZIP": "NO",
                     "PACKAGE_SKIP_CLEAN_INSTALL": "YES",
                     "PACKAGE_SKIP_CLEAN_OBJ": "YES",
                     "PACKAGE_SKIP_CLEAN_SRC_DIR": "YES"}

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
# install package

def install(i):
    """
    Input:  {
              (target)            - if specified, use info from 'machine' module
                 or
              (host_os)           - host OS (detect, if omitted)
              (target_os)         - target OS (detect, if omitted)
              (target_device_id)  - target device ID (detect, if omitted)

              (data_uoa) or (uoa) - package UOA entry
                       or
              (tags)              - tags to search package if data_uoa=='' before searching in current path
              (or_tags)           - add entries which has groups of tags separated by ;
              (no_tags)           - exclude entris with these tags separated by comma

              (env_data_uoa)      - use this data UOA to record (new) env
              (env_repo_uoa)      - use this repo to record new env

              (install_path)      - full path with soft is installed
              (path)              - path with soft is installed (path from the package will be appended)

              (skip_process)      - if 'yes', skip archive processing
              (skip_setup)        - if 'yes', skip environment setup

              (deps)              - pre-set some deps, for example for compiler

              (reuse_deps)           - if 'yes' reuse all deps if found in cache by tags
              (deps_cache)           - list with resolved deps

              (deps.{KEY})        - set deps[KEY]["uoa']=value (user-friendly interface via CMD to set any given dependency)
              (preset_deps)       - dict with {"KEY":"UOA"} to preset dependencies

              (param)             - string converted into CK_PARAM and passed to processing script
              (params)            - dict, keys are converted into <KEY>=<VALUE> and passed to processing script

              (env)               - add environment vars
              (env.{KEY})         - set env[KEY]=value (user-friendly interface via CMD)

              (Dkey)              - update params[key], i.e. ck install package:... -DENV1=val1 -DENV2=val2 (similar to CMAKE)

              (extra_version)     - add extra version, when registering software 
                                    (for example, -trunk-20160421)

              (extra_tags)        - add extra tags to separated customized packages (string separated by comma)

              (extra_path)        - add extra path to the automatically prepared one
                                    (for example, -trunk-20160421)

              (record_script)     - record tmp installation script with pre-set environment
                                    (to be able to call it to rebuild package without CK)

              (force_version)     - force version (useful for automatic installation of packages with multiple supported version)

              (install_to_env)    - install this package and all dependencies to env instead of CK-TOOLS (to keep it clean)!

              (safe)              - safe mode when searching packages first instead of detecting already installed soft
                                    (to have more deterministic build)

              (add_hint)          - if 'yes', add hint that can skip package installation and detect soft instead

              (rebuild)           - if 'yes', attempt to set env to avoid downloading package again, just rebuild (if supported)
              (reinstall)         - if 'yes', also download package and then rebuild it ...

              (version_from)      - check version starting from ... (list of numbers)
              (version_to)        - check version up to ... (list of numbers)

              (ask)               - if 'yes', ask more questions, otherwise select default actions
              (ask_version)       - ask for the version of the package the user wants to install
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              env_data_uoa - if installed fine
              env_data_uid - if installed fine
            }

    """
    import os
    import time
    import copy

    o=i.get('out','')

    oo=''
    if o=='con':
       oo=o

    ask=i.get('ask','')

    xtags=i.get('tags','')
    xor_tags=i.get('or_tags','')
    xno_tags=i.get('no_tags','')

    reuse_deps=i.get('reuse_deps','')
    deps_cache=i.get('deps_cache',[])

    # Check if package_channel is specifies and add tag
    pchannel=ck.cfg.get('package_channel','')
    if pchannel!='':
       if xtags!='': xtags+=','
       xtags+='channel-'+pchannel

    start_time = time.time()

    # Check if target
    if i.get('target','')!='':
       r=ck.access({'action':'init',
                    'module_uoa':cfg['module_deps']['machine'],
                    'input':i})
       if r['return']>0: return r

    device_cfg=i.get('device_cfg',{})

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')

    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'host_os':hos,
                 'target_os':tos,
                 'device_cfg':device_cfg,
                 'target_device_id':tdid,
                 'skip_info_collection':'yes'})
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    host_add_path_string=r.get('host_add_path_string','')

    hosn=hosd.get('ck_name2','')
    osn=tosd.get('ck_name2','')

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

    ck_os_name=hosd['ck_name']
    tname2=tosd['ck_name2']

    vfrom=i.get('version_from',[])
    vto=i.get('version_to',[])

    if type(vfrom)!=list:
       rx=ck.access({'action':'split_version',
                     'module_uoa':cfg['module_deps']['soft'],
                     'version':vfrom})
       if rx['return']>0: return rx
       vfrom=rx['version_split']

    if type(vto)!=list:
       rx=ck.access({'action':'split_version',
                     'module_uoa':cfg['module_deps']['soft'],
                     'version':vto})
       if rx['return']>0: return rx
       vto=rx['version_split']

    rem=hosd.get('rem','')
    eset=hosd.get('env_set','')
    svarb=hosd.get('env_var_start','')
    svare=hosd.get('env_var_stop','')
    scall=hosd.get('env_call','')
    sdirs=hosd.get('dir_sep','')
    sext=hosd.get('script_ext','')
    evs=hosd.get('env_var_separator','')
    eifs=hosd.get('env_quotes_if_space','')
    eifsc=hosd.get('env_quotes_if_space_in_call','')
    wb=tosd.get('windows_base','')

    iev=i.get('install_to_env','')
    if iev=='':
       iev=ck.cfg.get('install_to_env','')

    safe=i.get('safe','')

    rebuild=i.get('rebuild','')
    reinstall=i.get('reinstall','')

    # Check package description
    duoa=i.get('uoa','')
    if duoa=='': duoa=i.get('data_uoa','')
    duid=''
    dname=''
    d={}

    if duoa=='' and xtags=='':
       # Try to detect CID in current path
       rx=ck.detect_cid_in_current_path({})
       if rx['return']==0:
          duoa=rx.get('data_uoa','')

    if duoa!='':
       rx=ck.access({'action':'load',
                     'module_uoa':work['self_module_uid'],
                     'data_uoa':duoa})
       if rx['return']>0: return rx
       d=rx['dict']
       p=rx['path']

       duoa=rx['data_uoa']
       duid=rx['data_uid']
    else:
       # First, search by tags
       if xtags!='':
          r=ck.access({'action':'search',
                       'module_uoa':work['self_module_uid'],
                       'add_info':'yes',
                       'add_meta':'yes',
                       'tags':xtags})
          if r['return']>0: return r
          l=r['lst']
          if len(l)>0:
             # Check that support host/target OS
             ll=[]

             for q in l:
                 # Check if restricts dependency to a given host or target OS
                 rx=ck.access({'action':'check_target',
                               'module_uoa':cfg['module_deps']['soft'],
                               'dict':q.get('meta',{}),
                               'host_os_uoa':hosx,
                               'host_os_dict':hosd,
                               'target_os_uoa':tosx,
                               'target_os_dict':tosd})
                 if rx['return']==0:
                    # Split version
                    ver=q.get('meta',{}).get('customize',{}).get('version','')
                    if ver!='':
                       rx=ck.access({'action':'split_version',
                                     'module_uoa':cfg['module_deps']['soft'],
                                     'version':ver})
                       if rx['return']>0: return rx
                       sver=rx['version_split']

                       q['meta']['customize']['version_split']=sver

                    ll.append(q)

             # Prune by no_tags
             if xno_tags!='' or xor_tags!='' or len(vfrom)>0 or len(vto)>0:
                rx=ck.access({'action':'prune_search_list',
                              'module_uoa':cfg['module_deps']['env'],
                              'lst':ll,
                              'version_from':vfrom,
                              'version_to':vto,
                              'or_tags':xor_tags,
                              'no_tags':xno_tags})
                if rx['return']>0: return rx
                ll=rx['lst']

             # Select package 
             if len(ll)>0:
                # Sort by name and version
                l=sorted(ll, key=lambda k: (k.get('meta',{}).get('sort', 0),
                                            internal_get_val(k.get('meta',{}).get('customize',{}).get('version_split',[]), 0, 0),
                                            internal_get_val(k.get('meta',{}).get('customize',{}).get('version_split',[]), 1, 0),
                                            internal_get_val(k.get('meta',{}).get('customize',{}).get('version_split',[]), 2, 0),
                                            internal_get_val(k.get('meta',{}).get('customize',{}).get('version_split',[]), 3, 0),
                                            internal_get_val(k.get('meta',{}).get('customize',{}).get('version_split',[]), 4, 0),
                                            k.get('info',{}).get('data_name',''),
                                            k['data_uoa']),
                         reverse=True)

                il=0
                if len(l)>1:
                   ck.out('')
                   ck.out('More than one package found:')
                   ck.out('')
                   if i.get('add_hint','')=='yes':
                     ck.out('    (HINT: enter -1 to skip CK package installation and attemt to detect installed soft)')
                     ck.out('')

                   zz={}
                   iz=0
                   for z1 in l:
                       z=z1['data_uid']
                       zu=z1['data_uoa']

                       dn=z1.get('info',{}).get('data_name','')
                       if dn=='': dn=zu

                       dmeta=z1.get('meta',{})

                       ver=''
                       x=dmeta.get('customize',{}).get('version','')
                       if x!='': ver='  Version '+x+' '

                       zs=str(iz)
                       zz[zs]=z

                       # If has short comment
                       z1=dmeta.get('comment','')
                       if z1!='':
                          z1+=', '

                       ck.out(zs+') '+dn+ver+' ('+z1+z+')')

                       iz+=1

                   ck.out('')
                   rx=ck.inp({'text':'Select package number (or Enter to select 0): '})
                   ll=rx['string'].strip()
                   if ll=='': ll='0'

                   if ll=='-1' and i.get('add_hint','')=='yes':
                      return {'return':16, 'error':'skipped package installation!'}

                   if ll not in zz:
                      return {'return':1, 'error':'package number is not recognized'}

                   zduid=zz[ll]
                   for il in range(0, len(l)):
                       if l[il]['data_uid']==zduid: break

                   ck.out('')

                duid=l[il].get('data_uid','')
                duoa=duid
                duoax=l[il].get('data_uoa','')

                d=l[il]['meta']
                p=l[il]['path']

                if o=='con':
                   ck.out('')
                   ck.out('  Package found: '+duoax+' ('+duid+')')
                   ck.out('')

       if duoa=='' and xtags=='':
          found=False

          # Attempt to load configuration from the current directory
          try:
              p=os.getcwd()
          except OSError:
              os.chdir('..')
              p=os.getcwd()

          pc=os.path.join(p, ck.cfg['subdir_ck_ext'], ck.cfg['file_meta'])

          if os.path.isfile(pc):
             r=ck.load_json_file({'json_file':pc})
             if r['return']==0:
                d=r['dict']
                found=True

          if not found:
             return {'return':1, 'error':'package UOA (data_uoa) is not defined'}

       if duoa=='':
          x=''
          if xor_tags!='':
             x='and with or_tags="'+xor_tags+'" '
          if xno_tags!='':
             x='and with no_tags="'+xno_tags+'" '
          return {'return':16, 'error':'package with tags "'+xtags+'" '+x+'for your environment was not found!'}

    # Check if restricts dependency to a given host or target OS
    rx=ck.access({'action':'check_target',
                  'module_uoa':cfg['module_deps']['soft'],
                  'dict':d,
                  'host_os_uoa':hosx,
                  'host_os_dict':hosd,
                  'target_os_uoa':tosx,
                  'target_os_dict':tosd})
    if rx['return']>0: return rx

    # Get main params
    tags=copy.deepcopy(d.get('tags',[]))

    x=i.get('extra_tags','').strip()
    if x!='':
       tags.extend(x.split(','))

    cus=d.get('customize',{})
    env=d.get('env',{})

    extra_version=i.get('extra_version', cus.get('extra_version','') )

    udeps=d.get('deps',{})

    depsx=i.get('deps',{})
    if len(depsx)>0: 
        # RECENT UPDATE: check that is correct
        # Update only those keys that are in soft deps
        for k in udeps:
            if k in depsx:
                udeps[k]=depsx[k]
#        udeps.update(depsx)

    preset_deps=i.get('preset_deps', {})
    for q in i:
        if q.startswith('deps.'):
           preset_deps[q[5:]]=i[q]
    for q in preset_deps:
        if q in udeps:
           udeps[q]['uoa']=preset_deps[q]

    suoa=d.get('soft_uoa','')

    dname=d.get('package_name','')

    ver=cus.get('version','')+extra_version
    extra_dir=cus.get('extra_dir','')

    # This environment will be passed to process scripts (if any)
    pr_env=cus.get('install_env',{})

    # Check if need to ask version - this is useful when
    # a package downloads specific file depending on the version
    # and it is also reflected in the installed path 
    # (see GCC universal installation)
    if d.get('ask_version','')=='yes' and i.get('force_version','')=='':
       ck.out('')
       r=ck.inp({'text':'Enter version of the package you would like to install: '})
       if r['return']>0: return r
       ver=r['string'].strip()

    # Force version
    if i.get('force_version','')!='':
       ver=i['force_version']

    pr_env['PACKAGE_VERSION']=ver

    tags.append('host-os-'+hosx)
    tags.append('target-os-'+tosx)
    tags.append(tbits+'bits')

    enruoa=i.get('env_repo_uoa','')
    enduoa=i.get('env_data_uoa','')
    enduid=i.get('env_data_uid','')

    # Update this env from CK kernel (for example, to decide what to use, git or https)
    pr_env.update(ck.cfg.get('install_env',{}))

    # Update this env from customize meta (for example to pass URL to download package)
#    pr_env.update(cus.get('install_env',{}))
#    I moved it up to record changed env!

    for kpe in pr_env:
        x=pr_env[kpe]
        if x==str(x):
           x=str(x).replace('$#sep#$',sdirs) 

           j=x.find('$#path_to_cid=')
           if j>=0:
              j1=x.find('#$',j+13)
              if j1>0:
                 xcid=x[j+14:j1]

                 # Try to resolve CID
                 rx=ck.access({'action':'find', 'cid':xcid})
                 if rx['return']>0: 
                    return {'return':rx['return'], 'error':'Can\'t find entry when processing install_env var "'+kpe+'" ('+rx['error']+')'}

                 rxp=rx['path']

                 x=x[:j]+rxp+x[j1+2:]
 
           pr_env[kpe]=x

    ##########################################################################################
    #
    # All of the following:
    #       * "original" directory of the current entry
    #       * directory of the entry pointed by 'use_scripts_from_another_entry'
    #       * directory of the entry pointed by 'use_preprocess_scripts_from_another_entry'
    # may have a customization python script defined by the name 'custom_script_name'[.py]
    #
    # The interface methods that will be optionally called (if the script provides them) are:
    #       * pre_path()
    #       * post_deps()
    #       * setup()
    #       * post_setup()
    #
    # In case both the "original" and the "other" directory contain the customization script,
    # each of the methods listed above will be attempted:
    #       * first in the "other" (typically representing the base entry)
    #       * and then in the "original" (typically representing the derived entry)
    #
    # The mechanism seems to be an attempt to perform multiple inheritance of the entries,
    # both 'use_scripts_from_another_entry' and 'use_preprocess_scripts_from_another_entry'
    # representing the parents.
    #
    ##########################################################################################
    custom_script_name=cfg.get('custom_script_name','custom')
    customization_script=None
    original_customization_script=None # original - always in the current directory of a package!

    main_scripts_path=p
    preprocess_scripts_path=main_scripts_path

    # Check if has original custom script
    rx=ck.load_module_from_path({'path':main_scripts_path, 'module_code_name':custom_script_name, 'skip_init':'yes'})
    if rx['return']==0: 
       original_customization_script=rx['code']

    x=d.get('use_scripts_from_another_entry',{})
    if len(x)>0:
       r=ck.access({'action':'find',
                    'module_uoa':   x.get('module_uoa', work['self_module_uid']),
                    'data_uoa':     x.get('data_uoa','')
                })
       if r['return']>0: return r
       main_scripts_path=r['path']
       preprocess_scripts_path=main_scripts_path # may change later via use_preprocess_scripts_from_another_entry

    x=d.get('use_preprocess_scripts_from_another_entry',{})
    if len(x)>0:
       r=ck.access({'action':'find',
                    'module_uoa':   x.get('module_uoa', work['self_module_uid']),
                    'data_uoa':     x.get('data_uoa','')
                })
       if r['return']>0: return r
       preprocess_scripts_path=r['path']

    # Check if has custom script
    if preprocess_scripts_path==main_scripts_path and original_customization_script:
       customization_script=original_customization_script
       original_customization_script=None
    else:
       rx=ck.load_module_from_path({'path':preprocess_scripts_path, 'module_code_name':custom_script_name, 'skip_init':'yes'})
       if rx['return']==0: 
          customization_script=rx['code']

    # Check if need host CPU params
    features={}
    if d.get('need_cpu_info','')=='yes':
       r=ck.access({'action':'detect',
                    'module_uoa':cfg['module_deps']['platform.cpu'],
                    'host_os':hos,
                    'target_os':hos})
       if r['return']>0: return r

       cpu_ft=r.get('features',{}).get('cpu',{})
       features.update(r.get('features',{}))

       pr_env['CK_HOST_CPU_NUMBER_OF_PROCESSORS']=cpu_ft.get('num_proc','1')

       # We may want to pass more info (including target CPU) ...

    # Set up extra vars
    pr_env['CK_TARGET_CPU_BITS']=tosd.get('bits','')
    pr_env['CK_HOST_OS_ID']=hosn
    pr_env['CK_TARGET_OS_ID']=osn

    # Check if need host GPGPU params
    # We need a question here ('out':oo), since there can be multiple available drivers and we need to let user select the right one
    if d.get('need_gpgpu_info','')=='yes':
       r=ck.access({'action':'detect',
                    'module_uoa':cfg['module_deps']['platform.gpgpu'],
                    'type':d.get('need_gpgpu_type',''),
                    'host_os':hos,
                    'target_os':hos,
                    'out':oo})
       if r['return']>0: return r

       features.update(r.get('features',{}))

    # Update env from input
    envx=i.get('env',{})

    for q in i:
        if q.startswith('env.'):
           envx[q[4:]]=i[q]

    if len(envx)>0:
       pr_env.update(envx)

    # Search by exact terms
    setup={'host_os_uoa':hos,
           'target_os_uoa':tos,
           'target_os_bits':tbits}
    if ver!='':
       setup['version']=ver

    # Resolve deps
    if cus.get('ignore_deps','')=='yes':
       udeps={}

    sdeps=''
    if len(udeps)>0:
       env_resolve_action_dict={
           'action':'resolve',
           'module_uoa':cfg['module_deps']['env'],
           'host_os':hos,
           'target_os':tos,
           'target_device_id':tdid,
           'repo_uoa':enruoa,
           'install_to_env':iev,
           'install_env':pr_env,
           'reuse_deps':reuse_deps,
           'deps_cache':deps_cache,
           'safe':safe,
           'deps':udeps}
       if o=='con': env_resolve_action_dict['out']='con'

       rx=ck.access(env_resolve_action_dict)
       if rx['return']>0: return rx
       sdeps=rx['bat']
       udeps=rx['deps'] # Update deps (add UOA)

    for q in udeps:
        v=udeps[q]
        if v.get('uoa','')!='':
           setup['deps_'+q]=v['uoa']

    # Check installation path
    pre_path=i.get('path','')
    pi=i.get('install_path','')
    ep=i.get('extra_path','')
    fp=i.get('full_path','')

    x=cus.get('input_path_example','')
    if x!='': pie=' (example: '+ye+')'
    else: pie=''

    # If rebuild option, try to set vars to avoid download 
    if rebuild=='yes': pr_env.update(fix_env_for_rebuild)

    # Customize installation before installation path is finalized ******************************************************
    param_dict_for_pre_path={"host_os_uoa":hosx,
        "host_os_uid":hos,
        "host_os_dict":hosd,
        "target_os_uoa":tosx,
        "target_os_uid":tos,
        "target_os_dict":tosd,
        "target_device_id":tdid,
        "cfg":d,
        "tags":tags,
        "env":env,
        "install_env":pr_env,
        "deps":udeps,
        "customize":cus,
        "self_cfg":cfg,
        "features":features,
        "version":ver,
        "ck_kernel":ck
       }

    if o=='con': param_dict_for_pre_path['interactive']='yes'
    if i.get('quiet','')=='yes': param_dict_for_pre_path['interactive']=''

    rx = internal_run_if_present(customization_script, 'pre_path', param_dict_for_pre_path, pr_env)
    if rx['return']>0: return rx

    rx = internal_run_if_present(original_customization_script, 'pre_path', param_dict_for_pre_path, pr_env)
    if rx['return']>0: return rx

    dep_tags = []

    # Iterate through all dependencies and check which tags we need to create from them,
    #   preserving the desired sort order:
    #
    for dep_name, dep_dict in sorted(udeps.items(), key=lambda pair: pair[1].get('sort',0)) :
        if dep_name in ('compiler', 'host-compiler') :
            dep_tag_prefix  = 'compiled-by-'
        elif dep_dict.get('add_to_tags', dep_dict.get('add_to_path','') ):
            dep_tag_prefix = 'needs-'
        else:
            dep_tag_prefix = ''

        # Empty prefix means we don't want this dependency to appear in tags:
        #
        if dep_tag_prefix:
            dep_tag     = dep_tag_prefix + dep_dict.get('build_dir_name','unknown_' + dep_name)
            dep_tags.append( dep_tag )

            dep_version = dep_dict.get('ver')
            if dep_version:
                dep_tags.append( dep_tag + '-' + dep_version )

    # Join stripped tags and compiler tags into a CSV string:
    stripped_tags   = [t.strip() for t in tags if t.strip()]
    tags_csv        = ','.join( dep_tags + stripped_tags )

    xprocess    = i.get('skip_process','')!='yes' or rebuild=='yes' or reinstall=='yes'

    xsetup      = i.get('skip_setup','')!='yes' and d.get('skip_setup','')!='yes'

    shell_script_name=d.get('process_script','')
    if pi=='':
       # Check if environment already exists to check installation path
       if enduoa=='':
          if o=='con':
             ck.out('')
             ck.out('Searching if CK environment for this package already exists using:')
             ck.out('  * Tags: '+tags_csv)
             if len(udeps)>0:
                for q in udeps:
                    v=udeps[q]
                    vuoa=v.get('uoa','')
                    if vuoa!='':
                       ck.out('  * Dependency: '+q+'='+v.get('uoa',''))

          r=ck.access({'action':'search',
                       'module_uoa':cfg['module_deps']['env'],
                       'tags':tags_csv,
                       'search_dict':{'setup':setup}})
          if r['return']>0: return r
          lst=r['lst']

          # If more than one entry, try to prune by package UID if exists
          if duid!='':
             new_lst=[]
             for je in lst:
                 skip=False
                 rje=ck.access({'action':'load',
                                'module_uoa':cfg['module_deps']['env'],
                                'data_uoa':je['data_uid'],
                                'repo_uoa':je['repo_uid']})
                 if rje['return']==0:
                    print (rje['dict'].get('customize',{}).get('used_package_uid',''))
                    print (duid)

                    if rje['dict'].get('customize',{}).get('used_package_uid','')!=duid:
                       skip=True

                 if not skip:
                    new_lst.append(je)

             lst=new_lst

          if len(lst)==1:
             fe=lst[0]

             enruoa=fe['repo_uid']
             enduoa=fe['data_uoa']
             enduid=fe['data_uid']

             if iev=='yes':
                pi=fe['path']

             if o=='con':
                x=enduoa
                if enduid!=enduoa: x+=' ('+enduid+')'

                ck.out('')
                ck.out('CK environment found for this package: '+x)
          elif len(lst)>1:
             ck.out('')
             ck.out('AMBIGUITY: more than one environment entry found for this installation')

             ck.out('')
             for je in lst:
                 ck.out(' * '+je['data_uid'])
             ck.out('')

             return {'return':1, 'error':'more than one environment entry found for this installation, please specify using --env_data_uoa={correct environment entry UID}'}
          else:
             if o=='con':
                ck.out('')
                ck.out('CK environment not found for this package ...')

       # Load env if exists
       if enduoa!='':
          r=ck.access({'action':'load',
                       'module_uoa':cfg['module_deps']['env'],
                       'repo_uoa':enruoa,
                       'data_uoa':enduoa})
          if r['return']>0: return r
          de=r['dict']

          x=de.get('customize',{}).get('path_install','')
          if x!='': pi=x

          x=de.get('customize',{}).get('full_path','')
          if x!='': fp=x

#          if extra_dir!='':
#             j=pi.rfind(extra_dir)
#             if j>=0:
#                pi=pi[:j]
#
#             if pi!='':
#                j=len(pi)
#                if pi[j-1]==sdirs:
#                   pi=pi[:-1]


          if fp!='':
             if o=='con':

                if ask=='yes' and xprocess:
                   ck.out('')
                   ck.out('It appears that package is already installed or at least file from the package is already found in path: '+fp)

                   if shell_script_name:
                      ck.out('')
                      rx=ck.inp({'text':'Would you like to overwrite and process it again (y/N)? '})
                      x=rx['string'].strip().lower()
                      if x!='y' and x!='yes':
                         xprocess=False

                if ask=='yes' and xsetup:
                   ck.out('')
                   rx=ck.inp({'text':'Would you like to setup environment for this package again (Y/n)? '})
                   x=rx['string'].strip().lower()
                   if x=='n' or x=='no':
                      xsetup=False

                if ask!='yes' and xprocess:
                   ck.out('')
                   ck.out('  OVERWRITING AND PROCESSING AGAIN!')

             else:
                return {'return':1, 'error':'package is already installed in path '+pi}

       if enduoa=='' and iev=='yes':
          # Create dummy env and then set path there
          # TBD - if installation fails, we still have this dummy - need to check what to do ...
          #  can remove: ck rm env:* --tags=tmp
          xx=tags_csv
          if xx!='': xx+=','
          xx+='tmp'
          rx=ck.access({'action':'add',
                        'module_uoa':cfg['module_deps']['env'],
                        'repo_uoa':enruoa,
                        'tags':xx,
                        'dict':{'setup':setup}})
          if rx['return']>0: return rx

          enduoa=rx['data_uoa']
          enduid=rx['data_uid']
          pi=rx['path']

       if cus.get('skip_path','')!='yes' and pi=='':
          if o=='con':
             ck.out('')

          pix=''
          sp=d.get('suggested_path','')

          if pre_path=='':
             rz=prepare_install_path({})
             if rz['return']>0: return rz
             x=rz['path']
          else:
             x=pre_path

          if x!='' and sp!='':
             # Prepare installation path
             # First via package + version
             nm=sp

#             if cus.get('no_ver_in_suggested_path','')!='yes' and cus.get('version','')!='':
#                nm+='-'+cus.get('version','')
             if cus.get('no_ver_in_suggested_path','')!='yes' and ver!='':
                nm+='-'+ver

             # Then if compiler
             bdn=udeps.get('compiler',{}).get('build_dir_name','')
             vr=udeps.get('compiler',{}).get('ver','')
             if bdn=='':
                bdn=udeps.get('support_compiler',{}).get('build_dir_name','')
                vr=udeps.get('support_compiler',{}).get('ver','')

             if cus.get('no_compiler_in_suggested_path','')!='yes' and bdn!='':
                nm+='-'+bdn
                if vr!='':
                   nm+='-'+vr

             # Then any deps with explicitly specified 'add_to_path'
             for u in sorted(udeps, key=lambda v: udeps[v].get('sort',0)):
                 uu=udeps[u]
                 if uu.get('add_to_path','')=='yes':
                    vr=uu.get('ver','')

                    softuoa=uu.get('dict',{}).get('soft_uoa','')
                    salias=uu.get('dict',{}).get('soft_alias','')
                    if salias=='': salias=softuoa

                    if salias!='':
                       nm+='-'+salias
                    if vr!='':
                       nm+='-'+vr

             # Then some extra path, if non-empty
             nm += cus.get('extra_suggested_path','')

             # Then another extra path, if non-empty
             nm += ep

             # Finally OS
             if cus.get('no_os_in_suggested_path','')!='yes':
                nm+='-'+tosx

             pix=os.path.join(x, nm)
             if cus.get('no_os_in_suggested_path','')!='yes':
                if not tosx.endswith(tbits): pix+='-'+tbits

             if o=='con' and (ask=='yes' or cus.get('force_ask_path','')=='yes'):
                ck.out('*** Suggested installation path: '+pix)
                r=ck.inp({'text':'  Press Enter to use suggested path or input new installation path '+pie+': '})
                pi=r['string'].strip()
                if pi=='': pi=pix
             else:
                pi=pix
                if d.get('no_install_path','')!='yes':
                   ck.out('*** Installation path used: '+pix)

             if o=='con':
                ck.out('')

          else:
             if o=='con':
                r=ck.inp({'text':'Enter installation path '+pie+': '})
                pi=r['string'].strip()

       if pi=='' and cus.get('skip_path','')!='yes':
          return {'return':1, 'error':'installation path is not specified'}

    # Check dependencies
    deps={}
    dx={}
    if suoa!='':
       rx=ck.access({'action':'load',
                     'module_uoa':cfg['module_deps']['soft'],
                     'data_uoa':suoa})
       if rx['return']>0: return rx
       dx=rx['dict']
       deps=dx.get('deps',{})

    # Check package names
    if dname=='':
       dname=dx.get('soft_name','')

       if d.get('package_extra_name','')!='':
          cus['package_extra_name']=d['package_extra_name']

       if cus.get('package_extra_name','')!='':
          dname+=cus['package_extra_name']

    # Save package UOA to the cus
    cus['used_package_uoa']=duoa
    cus['used_package_uid']=duid

    # Update by package deps (more precise)
    for q in deps:
        v=deps[q]
        if q not in udeps:
           udeps[q]=v

    # Prepare environment based on deps
    if cus.get('ignore_deps','')=='yes':
       udeps={}

    sdeps=''
    if len(udeps)>0:
       env_resolve_action_dict={'action':'resolve',
           'module_uoa':cfg['module_deps']['env'],
           'host_os':hos,
           'target_os':tos,
           'target_device_id':tdid,
           'repo_uoa':enruoa,
           'install_to_env':iev,
           'reuse_deps':reuse_deps,
           'deps_cache':deps_cache,
           'safe':safe,
           'deps':udeps}
       if o=='con': env_resolve_action_dict['out']='con'

       rx=ck.access(env_resolve_action_dict)
       if rx['return']>0: return rx
       sdeps=rx['bat']

    if o=='con' and pi!='':
       ck.out('')
       ck.out('Installing to '+pi)
       ck.out('')

    # Customize installation based on resolved dependencies *************************************************************
    param_dict_for_post_deps={"host_os_uoa":hosx,
        "host_os_uid":hos,
        "host_os_dict":hosd,
        "target_os_uoa":tosx,
        "target_os_uid":tos,
        "target_os_dict":tosd,
        "target_device_id":tdid,
        "cfg":d,
        "tags":tags,
        "env":env,
        "features":features,
        "customize":cus,
        "self_cfg":cfg,
        "version":ver,
        "ck_kernel":ck,
        "deps":udeps
       }

    if o=='con': param_dict_for_post_deps['interactive']='yes'
    if i.get('quiet','')=='yes': param_dict_for_post_deps['interactive']=''

    rx = internal_run_if_present(customization_script, 'post_deps', param_dict_for_post_deps, pr_env)
    if rx['return']>0: return rx

    rx = internal_run_if_present(original_customization_script, 'post_deps', param_dict_for_post_deps, pr_env)
    if rx['return']>0: return rx

    soft_cfg={}

    # Check if continue processing
    if (shell_script_name or (customization_script and 'setup' in dir(customization_script))) and xprocess:
       # start bat
       shell_wrapper_contents=hosd.get('batch_prefix','')+'\n'

       if host_add_path_string!='':
          shell_wrapper_contents+=host_add_path_string+'\n\n'

       # Check if extra params to pass as environment
       param=i.get('param',None)
       params=d.get('params',{})
       params.update(i.get('params',{}))

       # Parse -D ...
       for k in i:
           if k.startswith('D'):
              params[k[1:]]=i[k]

       if param!=None:
          shell_wrapper_contents+='\n'
          xs=''
          if param.find(' ')>=0 and eifs!='': xs=eifs
          shell_wrapper_contents+=eset+' CK_PARAM='+xs+param+xs+'\n'

       if len(params)>0:
          for q in params:
              v=params[q]
              if v!=None:
                 xs=''
                 if v.find(' ')>=0 and eifs!='': xs=eifs
                 shell_wrapper_contents+=eset+' '+q+'='+xs+v+xs+'\n'

       shell_wrapper_contents+='\n'

       # Check installation path
       if pi=='' and cus.get('skip_path','')!='yes':
          if o=='con':
             ck.out('')

             pix=''
             sp=d.get('suggested_path','')

             rz=prepare_install_path({})
             if rz['return']>0: return rz
             x=rz['path']

             if x!='' and sp!='':
                pix=os.path.join(x, sp+'-'+cus.get('version','')+'-'+tosx)
                if not tosx.endswith(tbits): pix+='-'+tbits
                ck.out('Suggested path: '+pix)
                r=ck.inp({'text':'  Press Enter to use suggested path or input new installation path '+pie+': '})
                pi=r['string'].strip()
                if pi=='': pi=pix
             else:
                r=ck.inp({'text':'Enter installation path '+pie+': '})
                pi=r['string'].strip()

          if pi=='':
             return {'return':1, 'error':'installation path is not specified'}

       # Check if there is already library or tool exists
       x=d.get('end_full_path_universal','')
       if x=='':
          x=d.get('end_full_path',{}).get(tname2,'')
       fp=pi
       cont=True
       if x!='':
          x=x.replace('$#sep#$', sdirs)
          x=x.replace('$#abi#$', tosd.get('abi',''))
          x=x.replace('$#processor#$', tosd.get('processor',''))

            # NOTE: adapted from module/soft/module.py/prepare_target_name()
            #       After successful testing this function should be moved out
            #       into a common utility space and imported from there.
            #       Also, check whether the original function was supposed to be
            #           sourcing the data from hosd or tosd.
          file_extensions=tosd.get('file_extensions',{})
          for k in file_extensions:
              v=file_extensions[k]
              x=x.replace('$#file_ext_'+k+'#$',v)

          host_file_extensions=hosd.get('host_file_extensions',{})
          for k in host_file_extensions:
              v=host_file_extensions[k]
              x=x.replace('$#host_file_ext_'+k+'#$',v)

          fp=os.path.join(fp,x)
          if os.path.isfile(fp):
             if o=='con':
                ck.out('')
                ck.out('It appears that package is already installed or at least file from the package is already found in path: '+fp)

                if (rebuild!='yes' and reinstall!='yes') or ask=='yes':
                   ck.out('')
                   rx=ck.inp({'text':'Would you like to overwrite/process it again (y/N)? '})
                   x=rx['string'].strip().lower()
                   if x!='y' and x!='yes':
                      cont=False
                else:
                   ck.out('')
                   ck.out('  OVERWRITING AND PROCESSING AGAIN!')


       # Check if need to use scripts from another entry
       if cont:
          # Customize main installation
          param_dict_for_setup={"host_os_uoa":hosx,
              "host_os_uid":hos,
              "host_os_dict":hosd,
              "target_os_uoa":tosx,
              "target_os_uid":tos,
              "target_os_dict":tosd,
              "target_device_id":tdid,
              "cfg":d,
              "tags":tags,
              "env":env,
              "new_env":pr_env,
              "deps":udeps,
              "features":features,
              "customize":cus,
              "self_cfg":cfg,
              "version":ver,
              "path":main_scripts_path,
              "path_original_package":p,
              "script_path":preprocess_scripts_path,
              "out":oo,
              "install_path":pi
             }

          if o=='con': param_dict_for_setup['interactive']='yes'
          if i.get('quiet','')=='yes': param_dict_for_setup['interactive']=''

          param_dict_for_post_setup=copy.deepcopy(param_dict_for_setup)

          param_dict_for_post_setup['ck_kernel']=ck
          param_dict_for_setup['ck_kernel']=ck

          rx = internal_run_if_present(customization_script, 'setup', param_dict_for_setup, pr_env)
          if rx['return']>0: return rx
          else:
                soft_cfg=rx.get('soft_cfg',{})

          rx = internal_run_if_present(original_customization_script, 'setup', param_dict_for_setup, pr_env)
          if rx['return']>0: return rx

          # Prepare process script
          if shell_script_name:
             shell_script_name+=sext
             shell_script_full_path=os.path.join(main_scripts_path,shell_script_name)

             if not os.path.isfile(shell_script_full_path):
                return {'return':1, 'error':'processing script '+shell_script_name+' is not found'}

             # Add deps if needed before running
             if sdeps!='':
                shell_wrapper_contents+=sdeps

             # Add compiler dep again, if there
             for k in sorted(udeps, key=lambda v: udeps[v].get('sort',0)):
                 if 'compiler' in k:
                    x=udeps[k].get('bat','').strip()
                    if x!='' and not shell_wrapper_contents.endswith(x):
                       shell_wrapper_contents+='\n'+x+' 1\n\n'

             # Add misc environment (prepared above)
             for q in pr_env:
                 qq=str(pr_env[q])

                 qq=qq.replace('$<<',svarb).replace('>>$',svare)

                 if qq.find(' ')>0:
                    qq=eifs+qq+eifs
                 shell_wrapper_contents+=eset+' '+q+'='+qq+'\n'

             # If install path has space, add quotes for some OS ...
             xs=''
             if pi.find(' ')>=0 and eifs!='': xs=eifs
             shell_wrapper_contents+=eset+' INSTALL_DIR='+xs+pi+xs+'\n'

             # If Windows, add MingW path
             if wb=='yes':
                rm=ck.access({'action':'convert_to_cygwin_path',
                              'module_uoa':cfg['module_deps']['os'],
                              'path':pi})
                if rm['return']>0: return rm
                ming_pi=rm['path']
                shell_wrapper_contents+=eset+' INSTALL_DIR_MINGW='+xs+ming_pi+xs+'\n'

             xs=''
             if p.find(' ')>=0 and eifs!='': xs=eifs
             shell_wrapper_contents+=eset+' PACKAGE_DIR='+xs+main_scripts_path+xs+'\n'

             # If Windows, add MingW path
             if wb=='yes':
                rm=ck.access({'action':'convert_to_cygwin_path',
                              'module_uoa':cfg['module_deps']['os'],
                              'path':main_scripts_path})
                if rm['return']>0: return rm
                ming_ppp=rm['path']
                shell_wrapper_contents+=eset+' PACKAGE_DIR_MINGW='+xs+ming_ppp+xs+'\n'

             xs=''
             if p.find(' ')>=0 and eifs!='': xs=eifs
             shell_wrapper_contents+=eset+' ORIGINAL_PACKAGE_DIR='+xs+p+xs+'\n'

             # If Windows, add MingW path
             if wb=='yes':
                rm=ck.access({'action':'convert_to_cygwin_path',
                              'module_uoa':cfg['module_deps']['os'],
                              'path':p})
                if rm['return']>0: return rm
                ming_p=rm['path']
                shell_wrapper_contents+=eset+' ORIGINAL_PACKAGE_DIR_MINGW='+xs+ming_p+xs+'\n'

             shell_wrapper_contents+='\n'

             xs=''
             if p.find(' ')>=0 and eifsc!='': xs=eifsc
             shell_wrapper_contents+=scall+' '+xs+shell_script_full_path+xs+'\n\n'

             if wb=='yes' and d.get('check_exit_status','')!='yes':
                shell_wrapper_contents+='exit /b 0\n'

             rs=i.get('record_script','')

             # Generate tmp file (or use record script)
             if rs:
                shell_wrapper_name=rs
                if shell_wrapper_name==os.path.basename(shell_wrapper_name):
                   shell_wrapper_name=os.path.join(os.getcwd(),shell_wrapper_name)
             else:
                rx=ck.gen_tmp_file({'prefix':'tmp-ck-', 'suffix':sext})
                if rx['return']>0: return rx
                shell_wrapper_name=rx['file_name']

             # Write to tmp file
             rx=ck.save_text_file({'text_file':shell_wrapper_name, 'string':shell_wrapper_contents})
             if rx['return']>0: return rx

             # Go to installation path
             if not os.path.isdir(pi):
                os.makedirs(pi)
             os.chdir(pi)

             # Check if need to set executable flags
             se=hosd.get('set_executable','')
             if se!='':
                x=se+' '+shell_wrapper_name
                rx=os.system(x)

             # Run script
             rx=os.system(shell_wrapper_name)

             # Remove script (if tmp)
             if rs=='' and os.path.isfile(shell_wrapper_name):
                os.remove(shell_wrapper_name)

             if rx>0: 
                return {'return':1, 'error':'package installation failed'}

          # Check if has post-setup Python script
          param_dict_for_post_setup['new_env']=pr_env

          rx = internal_run_if_present(customization_script, 'post_setup', param_dict_for_post_setup, {})
          if rx['return']>0: return rx

          rx = internal_run_if_present(original_customization_script, 'post_setup', param_dict_for_post_setup, {})
          if rx['return']>0: return rx

    # Preparing soft registration
    soft_registration_action_dict={'action':'setup',
        'module_uoa':cfg['module_deps']['soft'],
        'data_uoa':suoa,
        'soft_name':dname,
        'host_os':hos,
        'target_os':tos,
        'target_device_id':tdid,
        'tags':tags_csv,
        'customize':cus,
        'features':features,
        'env_new':'yes',
        'env_repo_uoa':enruoa,
        'env_data_uoa':enduoa,
        'env':env,
        'extra_version':extra_version
       }

    nw='no'
    if enduoa=='': nw='yes'

    if cus.get('collect_device_info','')!='yes':
        soft_registration_action_dict['skip_device_info_collection']='yes'

    if d.get('remove_deps','')=='yes':
       soft_registration_action_dict['deps_copy']=udeps
    else:
       soft_registration_action_dict['deps']=udeps

    if d.get('no_install_path','')!='yes':
       if fp!='':
          soft_registration_action_dict['full_path']=fp
          soft_registration_action_dict['full_path_install']=pi
       elif pi!='':              # mainly for compatibility with previous CK soft manager
          soft_registration_action_dict['install_path']=pi

    if duid!='': soft_registration_action_dict['package_uoa']=duid

    if len(soft_cfg)>0:
       soft_registration_action_dict.update(soft_cfg)

    ck_install_file_contents=copy.deepcopy(soft_registration_action_dict)

    # Check if need to setup environment
    if xsetup:
       if suoa=='':
          return {'return':1, 'error':'Software environment UOA is not defined in this package (soft_uoa)'}

#       if extra_dir!='':
#          pi+=sdirs+extra_dir

       x=d.get('end_full_path_universal','')
       if x=='':
          x=d.get('end_full_path',{}).get(tname2,'')
       fp=pi
       if x!='': 
          x=x.replace('$#sep#$', sdirs)
          x=x.replace('$#abi#$', tosd.get('abi',''))
          fp=os.path.join(fp,x)

       if suoa!='':
          if o=='con':
             ck.out('')
             ck.out('Setting up environment for installed package ...')
             ck.out('  (full path = '+fp+')')
             ck.out('')

          if o=='con': soft_registration_action_dict['out']='con'

          rx=ck.access(soft_registration_action_dict)
          if rx['return']>0: return rx

          enduoa=rx['env_data_uoa']
          enduid=rx['env_data_uid']

    # Recording cus dict to install dir to be able to rebuild env later if needed 
    if pi!='':
       ck_install_file_path=os.path.join(pi, cfg['ck_install_file'])

       if o=='con':
          ck.out('')
          ck.out('Recording CK configuration to '+ck_install_file_path+' ...')

       ck_install_file_contents['env_data_uoa']=enduid

       rx=ck.save_json_to_file({'json_file':ck_install_file_path, 'dict':ck_install_file_contents, 'sort_keys':'yes'})
       if rx['return']>0: return rx

    if o=='con' and pi!='':
       ck.out('')
       ck.out('Installation path: '+pi)
       ck.out('')

    elapsed_time=time.time()-start_time
    if o=='con':
       ck.out('Installation time: '+str(elapsed_time)+' sec.')

    return {'return':0, 'elapsed_time':elapsed_time, 'env_data_uoa':enduoa, 'env_data_uid':enduid}

##################################################################################
# internal function: run a method of a given customization script with param_dict
#                    and top up the topup_from_install_env dictionary from install_env

def internal_run_if_present(script, method_name, param_dict, topup_from_install_env):
    if script and method_name in dir(script):
        method = getattr(script, method_name)
        rx = method( param_dict )
        if rx.get('return')==0:
            topup_from_install_env.update( rx.get('install_env',{}) )
    else:
        rx = { 'return' : 0 };
    return rx

##############################################################################
# setup package (only environment)

def setup(i):
    """
    Input:  {
               See 'install' function
               skip_process=yes
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    i['skip_process']='yes'
    return install(i)

##############################################################################
# internal function: get value from list without error if out of bounds

def internal_get_val(lst, index, default_value):
    v=default_value
    if index<len(lst):
       v=lst[index]
    return v

##############################################################################
# rebuild dependencies using packages

def rebuild_deps(i):
    """
    Input:  {
              (target)            - if specified, use info from 'machine' module
                 or
              (host_os)           - host OS (detect, if omitted)
              (target_os)         - target OS (detect, if omitted)
              (target_device_id)  - target device ID (detect, if omitted)

              (data_uoa) or (uoa) - package UOA entry
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    o=i.get('out','')

    oo=''
    if o=='con':
       oo=o

    # Check if target
    if i.get('target','')!='':
       r=ck.access({'action':'init',
                    'module_uoa':cfg['module_deps']['machine'],
                    'input':i})
       if r['return']>0: return r

    device_cfg=i.get('device_cfg',{})

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')

    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'host_os':hos,
                 'target_os':tos,
                 'device_cfg':device_cfg,
                 'target_device_id':tdid,
                 'skip_info_collection':'yes'})
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    # Get list of deps
    duoa=i.get('data_uoa','')
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa})
    if r['return']>0: return r

    d=r['dict']

    deps=d.get('deps',{})

    for k in sorted(deps, key=lambda v: deps[v].get('sort',0)):
        dd=deps[k]
        dn=dd.get('name','')

        if dn=='':
            dn=k
        else:
            dn+=' ('+k+')'

        tags=dd.get('tags','')

        if oo=='con':
            ck.out('*******************************************************')
            ck.out('Dependency: '+dn)
            ck.out('Tags:       '+tags)
            ck.out('')

        ntos=tos
        if dd.get('force_target_as_host','')=='yes':
             ntos=hos

        # Attempt to install package by tags
        r=ck.access({'action':'install',
            'module_uoa':work['self_module_uid'],
            'tags':tags,
            'host_os':hos,
            'target_os':ntos,
            'device_id':tdid,
            'out':oo})
        if r['return']>0: 
           ck.out('')
           ck.out('Package installation failed: '+r['error']+'!')

    return {'return':0}

##############################################################################
# show available packages

def show(i):
    """
    Input:  {
               (the same as list; can use wildcards)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    o=i.get('out','')

    html=False
    if o=='html' or i.get('web','')=='yes':
       html=True

    h=''

    unique_repo=False
    if i.get('repo_uoa','')!='': unique_repo=True

    import copy
    list_action_dict=copy.deepcopy(i)

    list_action_dict['out']=''
    list_action_dict['action']='list'
    list_action_dict['add_meta']='yes'

    rx=ck.access(list_action_dict)
    if rx['return']>0: return rx

    ll=sorted(rx['lst'], key=lambda k: k['data_uoa'])

    if html:
       h+='<i><b>Note:</b> you can install package via <pre>$ ck install package:{package UOA} (--target_os=android21-arm64)</i><br><br>\n'
       h+='<table cellpadding="5">\n'

       h+=' <tr>\n'
       h+='  <td><b>CK&nbsp;module&nbsp;(aka&nbsp;wrapper,&nbsp;plugin&nbsp;or&nbsp;container):</b></td>\n'
       h+='  <td width="200"><b>CK Repository:</b></td>\n'
       h+='  <td><b>Description:</b></td>\n'
       h+=' </tr>\n'

    repo_url={}
    repo_private={}

    private=''
    for l in ll:
        ln=l['data_uoa']
        lr=l['repo_uoa']

        lr_uid=l['repo_uid']
        url=''
        if lr=='default':
           url='' #'http://github.com/ctuning/ck'
        elif lr_uid in repo_url:
           url=repo_url[lr_uid]
        else:
           rx=ck.load_repo_info_from_cache({'repo_uoa':lr_uid})
           if rx['return']>0: return rx
           url=rx.get('dict',{}).get('url','')
           repo_private[lr_uid]=rx.get('dict',{}).get('private','')
           repo_url[lr_uid]=url

        private=repo_private.get(lr_uid,'')

        if lr not in cfg.get('skip_repos',[]) and private!='yes':
           lm=l['meta']
           ld=lm.get('desc','')

           name=lm.get('soft_name','')

           cus=lm.get('customize',{})

           ver=cus.get('version','')

           xhos=lm.get('only_for_host_os_tags',[])
           xtos=lm.get('only_for_target_os_tags',[])

           tags=lm.get('tags',[])
           ytags=','.join(tags)

           yhos=''
           ytos=''

           for q in xhos:
               if yhos!='': yhos+=','
               yhos+=q

           for q in xtos:
               if ytos!='': ytos+=','
               ytos+=q

           if lr=='default':
              to_get=''
           elif url.find('github.com/ctuning/')>0:
              to_get='ck pull repo:'+lr
           else:
              to_get='ck pull repo --url='+url

           ###############################################################
           if html:
              h+=' <tr>\n'

              h+='  <td valign="top"><b>'+ln+'</b></td>\n'

              x1=''
              x2=''
              if url!='':
                 x1='<a href="'+url+'">'
                 x2='</a>'

              h+='  <td valign="top"><i>'+x1+lr+x2+'</i></td>\n'

              h+='  <td valign="top">'+ld+'\n'

              h+='</td>\n'

              h+=' </tr>\n'

           ###############################################################
           elif o=='mediawiki':
              x=lr
              y=''
              if url!='':
                 x='['+url+' '+lr+']'
                 y='['+url+'/tree/master/package/'+ln+' link]'
              ck.out('')
              ck.out('=== '+ln+' ('+ver+') ===')
              ck.out('')
              ck.out('Tags: <i>'+ytags+'</i>')
              ck.out('<br>Host OS tags: <i>'+yhos+'</i>')
              ck.out('<br>Target OS tags: <i>'+ytos+'</i>')
              if y!='':
                 ck.out('')
                 ck.out('Package entry with meta: <i>'+y+'</i>')
              ck.out('')
              ck.out('Which CK repo: '+x)
              if to_get!='':
                 ck.out('<br>How to get: <i>'+to_get+'</i>')
              if to_get!='':
                 ck.out('')
                 ck.out('How to install: <i>ck install package:'+ln+' (--target_os={CK OS UOA})</i>')
              ck.out('')

           ###############################################################
           elif o=='con' or o=='txt':
              if unique_repo:
                 ck.out('')
                 s=ln+' - '+ld

              else:
                 ss=''
                 if len(ln)<35: ss=' '*(35-len(ln))

                 ss1=''
                 if len(lr)<30: ss1=' '*(30-len(lr))

                 s=ln+ss+'  ('+lr+')'
                 if ld!='': s+=ss1+'  '+ld

              ck.out(s)


    if html:
       h+='</table>\n'

    return {'return':0, 'html':h}

##############################################################################
# prepare installation path

def prepare_install_path(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              path         - prepared path where to install packages
            }

    """

    import os

    # Moved Tools to $HOME by default if CK_TOOLS is not defined
    x=os.environ.get(cfg["env_install_path"],'')
    if x=='':
       # Get home user directory
       from os.path import expanduser
       home = expanduser("~")
       x=os.path.join(home, cfg["install_path"])
       if not os.path.isdir(x):
          os.makedirs(x)

    return {'return':0, 'path':x}

##############################################################################
# prepare distribution

def distribute(i):
    """
    Input:  {
              (data_uoa) - package UOA

              (ext)      - output package ext (ck-distro-{ext}).zip  If not specified, UID is generated.
                or
              (filename) - full name of output package

              (path_key) - (path_bin, path_lib, path_include)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import shutil

    # Init
    o=i.get('out','')

    oo=''
    if o=='con':
       oo=o

    cur_dir=os.getcwd()

    duoa=i.get('data_uoa','')
    tags=i.get('tags','')

    pk=i.get('path_key','')
    if pk=='': pk='path_bin'

    # Extension
    fn=i.get('filename','')
    if fn=='':
       ext=i.get('ext','')
       if ext=='':
          rx=ck.gen_uid({})
          if rx['return']>0: return rx
          ext=rx['data_uid']

       fn='ck-distro-'+ext+'.zip'

    # Check if target
    if i.get('target','')!='':
       r=ck.access({'action':'init',
                    'module_uoa':cfg['module_deps']['machine'],
                    'input':i})
       if r['return']>0: return r

    device_cfg=i.get('device_cfg',{})

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')

    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'host_os':hos,
                 'target_os':tos,
                 'device_cfg':device_cfg,
                 'target_device_id':tdid,
                 'skip_info_collection':'yes'})
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    host_add_path_string=r.get('host_add_path_string','')

    hosn=hosd.get('ck_name2','')
    osn=tosd.get('ck_name2','')

    # Load package meta
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa})
    if r['return']>0: return r
    d=r['dict']
    p0=r['path']

    # Get tags
    tags=d['tags']
    xtags=','.join(tags)

    # Resolve env
    if o=='con':
       ck.out('Searching environment for this package ...')

    r=ck.access({'action':'set',
                 'module_uoa':cfg['module_deps']['env'],
                 'tags':xtags,
                 'host_os':hos,
                 'target_os':tos,
                 'device_id':tdid,
                 'out':oo})
    if r['return']>0: return r

    de=r['dict']

    deps=de.get('deps',{})

    # Path
    cus=de.get('customize',{})
    pp=cus.get(pk,'')
    pp1=pp

    found=False
    while not found:
        pp1=os.path.dirname(pp)

        if pp1==pp:
           break

        ppx=os.path.join(pp1, cfg['ck_install_file'])
        if os.path.isfile(ppx):
           found=True
           break

        pp=pp1

    # Read ck-install.json
    if not found:
       return {'return':1, 'error':pp1+' not found in installation paths ...'}

    r=ck.load_json_file({'json_file':ppx})
    if r['return']>0: return r
    dx=r['dict']

    # Rename deps (to avoid mix ups with local env)
#    dx['saved_deps']=dx.pop('deps')

    # Save to tmp file
    rx=ck.gen_tmp_file({'prefix':'tmp-ck-', 'suffix':'.json'})
    if rx['return']>0: return rx
    ftmp=rx['file_name']

    r=ck.save_json_to_file({'json_file':ftmp, 'dict':dx, 'sort_keys':'yes'})
    if r['return']>0: return r

    # Check extra commands (for a given target platform)
    ec=d.get('distribute_extra_commands',{}).get(osn,[])

    for q in ec:
        if o=='con':
           ck.out('')
           ck.out('Executing extra command')
           ck.out('')

        q['out']=oo
        q['host_os']=hos
        q['target_os']=tos
        q['device_id']=tdid

        r=ck.access(q)
        if r['return']>0: return r

    # Check extra files (for a given target platform)
    ef=d.get('distribute_extra_file',{}).get(osn,[])

    r=get_paths_from_deps({'deps':deps})
    if r['return']>0: return r
    paths=r['paths']

    for q in ef:
        fx=q['file']

        if o=='con':
           ck.out('')
           ck.out('  * Searching extra file '+fx+' ...')

        where=q.get('where_key','')
        if where=='': where='path_bin'

        pzz=''

        muoa=q.get('module_uoa','')
        duoa=q.get('data_uoa','')
        if muoa!='' and duoa!='':
           r=ck.access({'action':'load',
                        'module_uoa':muoa,
                        'data_uoa':duoa})
           if r['return']>0: return r
           py=r['path']

           pi=q.get('extra_dir','')
           if pi!='': py=os.path.join(py,pi)

           pzz=os.path.join(py,fx)

        else:
           for py in paths:
               pz=os.path.join(py,fx)
               if os.path.isfile(pz):
                  pzz=pz
                  break

        if pzz=='':
           return {'return':1, 'error':'file not found'}

        if o=='con':
           ck.out('       Found ('+pzz+') - copying ...')

        pz1=cus.get(pk,'')

        if q.get('new_file','')!='': fx=q['new_file']

        pz2=os.path.join(pz1, fx)

        if os.path.isfile(pz2): os.remove(pz2)

        shutil.copyfile(pzz, pz2)

    # Check extra dirs (dist) in package
    px=os.path.join(p0,'dist')
    if os.path.isdir(px):
       if o=='con':
          ck.out('')
          ck.out('Copying extra dist directory ...')

       pxx=os.listdir(px)

       for q in pxx:
           q1=os.path.join(px,q)
           q2=os.path.join(pp,q)

           if o=='con':
              ck.out('  * '+q)

           if os.path.isdir(q2) or os.path.isfile(q2): 
              shutil.rmtree(q2)

           shutil.copytree(q1,q2)

    # Prepare zip
    import zipfile

    zip_method=zipfile.ZIP_DEFLATED

    r=ck.list_all_files({'path':pp})
    if r['return']>0: return r

    flx=r['list']

    # Write archive
    if o=='con':
       ck.out('')
       ck.out('Recording generated package to '+fn+' ...')

    pfn=os.path.join(cur_dir,fn)

    try:
       f=open(pfn, 'wb')
       z=zipfile.ZipFile(f, 'w', zip_method)

       for fn in flx:
           p1=os.path.join(pp, fn)
           z.write(p1, 'install'+os.sep+fn, zip_method)

       # ck-install.json
       z.write(ftmp, cfg['ck_install_file_saved'], zip_method)

       z.close()
       f.close()

    except Exception as e:
       return {'return':1, 'error':'failed to prepare archive ('+format(e)+')'}

    if os.path.isfile(ftmp):
       os.remove(ftmp)

    return {'return':0}

##############################################################################
# get all paths from deps

def get_paths_from_deps(i):
    """
    Input:  {
              (deps)  - deps
              (paths) - current list of paths
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    deps=i.get('deps',{})
    paths=i.get('paths',[])

    for k in sorted(deps, key=lambda v: deps[v].get('sort',0)):
        dp=deps[k]

        uoa=dp.get('uoa','')
        if uoa!='':
           r=ck.access({'action':'load',
                        'module_uoa':cfg['module_deps']['env'],
                        'data_uoa':uoa})
           if r['return']>0: return r
           dp1=r['dict']

           dpx=dp1.get('customize',{})

           x=dpx.get('path_bin','')
           if x!='' and x not in paths: paths.append(x)

           if x=='':
              # Trick for some dll on Windows
              x=dpx.get('path_lib','')
              if x!='':
                 x=os.path.dirname(x)
                 x=os.path.join(x,'bin')
                 if os.path.isdir(x) and x not in paths: paths.append(x)

           x=dpx.get('path_lib','')
           if x!='' and x not in paths: paths.append(x)
       
           x=dpx.get('path_include','')
           if x!='' and x not in paths: paths.append(x)

           ndpd=dp1.get('deps',{})
           if len(ndpd)>0:
              r=get_paths_from_deps({'deps':ndpd, 'paths':paths})
              if r['return']>0: return r
              paths=r['paths']

    return {'return':0, 'paths':paths}

##############################################################################
# reinstall package if already installed

def reinstall(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    i['reinstall']='yes'
    return install(i)
