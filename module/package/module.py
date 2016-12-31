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
              (no_tags)           - exclude entris with these tags separated by comma

              (env_data_uoa)      - use this data UOA to record (new) env
              (env_repo_uoa)      - use this repo to record new env

              (install_path)      - path with soft is installed
              (ask)               - if 'yes', ask path

              (skip_process)      - if 'yes', skip archive processing
              (skip_setup)        - if 'yes', skip environment setup

              (deps)              - pre-set some deps, for example for compiler

              (param)             - string converted into CK_PARAM and passed to processing script
              (params)            - dict, keys are onverted into <KEY>=<VALUE> and passed to processing script

              (env)               - add environment vars
              (env.{KEY})         - set env[KEY]=value (user-friendly interface via CMD)

              (Dkey)              - update params[key], i.e. ck install package:... -DENV1=val1 -DENV2=val2 (similar to CMAKE)

              (extra_version)     - add extra version, when registering software 
                                    (for example, -trunk-20160421)

              (extra_path)        - add extra path to the automatically prepared one
                                    (for example, -trunk-20160421)

              (record_script)     - record tmp installation script with pre-set environment
                                    (to be able to call it to rebuild package without CK)

              (force_version)     - force version (useful for automatic installation of packages with multiple supported version)

              (install_to_env)    - install this package and all dependencies to env instead of CK-TOOLS (to keep it clean)!
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


    o=i.get('out','')

    oo=''
    if o=='con':
       oo=o

    xtags=i.get('tags','')
    xno_tags=i.get('no_tags','')

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
             if xno_tags!='':
                rx=ck.access({'action':'prune_search_list',
                              'module_uoa':cfg['module_deps']['env'],
                              'lst':ll,
                              'no_tags':xno_tags})
                if rx['return']>0: return rx
                ll=rx['lst']

             # Select package 
             if len(ll)>0:
                # Sort by name and version
                l=sorted(ll, key=lambda k: (internal_get_val(k.get('meta',{}).get('customize',{}).get('version_split',[]), 0, 0),
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

                   zz={}
                   iz=0
                   for z1 in l:
                       z=z1['data_uid']
                       zu=z1['data_uoa']

                       dn=z1.get('info',{}).get('data_name','')
                       if dn=='': dn=zu

                       ver=''
                       x=z1.get('meta',{}).get('customize',{}).get('version','')
                       if x!='': ver='  Version '+x+' '

                       zs=str(iz)
                       zz[zs]=z

                       ck.out(zs+') '+dn+ver+' ('+z+')')

                       iz+=1

                   ck.out('')
                   rx=ck.inp({'text':'Select package number (or Enter to select 0): '})
                   ll=rx['string'].strip()
                   if ll=='': ll='0'

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
          return {'return':16, 'error':'package with such tags and for this environment was not found!'}

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
    tags=d.get('tags',[])
    cus=d.get('customize',{})
    env=d.get('env',{})

    ev=i.get('extra_version','')
    if ev=='':
       ev=cus.get('extra_version','')

    udeps=d.get('deps',{})

    depsx=i.get('deps',{})
    if len(depsx)>0: 
        # RECENT UPDATE: check that is correct
        # Update only those keys that are in soft deps
        for k in udeps:
            if k in depsx:
                udeps[k]=depsx[k]
#        udeps.update(depsx)

    suoa=d.get('soft_uoa','')

    dname=d.get('package_name','')
    edname=d.get('package_extra_name','')

    ver=cus.get('version','')+ev
    extra_dir=cus.get('extra_dir','')

    # This environment will be passed to process scripts (if any)
    pr_env={}

    # Check if need to ask version - this is useful when
    # a package downloads specific file depending on the version
    # and it is also reflected in the installed path 
    # (see GCC universal installation)
    if d.get('ask_version','')=='yes':
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
    pr_env.update(cus.get('install_env',{}))

    for kpe in pr_env:
        pr_env[kpe]=pr_env[kpe].replace('$#sep#$',sdirs) 

    # Check if has customized script
    ppp=p
    ppp1=ppp # Preprocess scripts

    x=d.get('use_scripts_from_another_entry',{})
    if len(x)>0:
       xam=x.get('module_uoa','')
       if xam=='': xam=work['self_module_uid']
       xad=x.get('data_uoa','')
       r=ck.access({'action':'find',
                    'module_uoa':xam,
                    'data_uoa':xad})
       if r['return']>0: return r
       ppp=r['path']
       ppp1=ppp # can be changed later via use_preprocess_scripts_from_another_entry

    x=d.get('use_preprocess_scripts_from_another_entry',{})
    if len(x)>0:
       xam=x.get('module_uoa','')
       if xam=='': xam=work['self_module_uid']
       xad=x.get('data_uoa','')
       r=ck.access({'action':'find',
                    'module_uoa':xam,
                    'data_uoa':xad})
       if r['return']>0: return r
       ppp1=r['path']

    # Check if has custom script
    cs=None
    csn=cfg.get('custom_script_name','custom')
    rx=ck.load_module_from_path({'path':ppp1, 'module_code_name':csn, 'skip_init':'yes'})
    if rx['return']==0: 
       cs=rx['code']

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

    # Check if need host GPGPU params
    if d.get('need_gpgpu_info','')=='yes':
       r=ck.access({'action':'detect',
                    'module_uoa':cfg['module_deps']['platform.gpgpu'],
                    'type':d.get('need_gpgpu_type',''),
                    'host_os':hos,
                    'target_os':hos})
#                    'out':oo})
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
       ii={'action':'resolve',
           'module_uoa':cfg['module_deps']['env'],
           'host_os':hos,
           'target_os':tos,
           'target_device_id':tdid,
           'repo_uoa':enruoa,
           'install_to_env':iev,
           'deps':udeps}
       if o=='con': ii['out']='con'

       rx=ck.access(ii)
       if rx['return']>0: return rx
       sdeps=rx['bat']
       udeps=rx['deps'] # Update deps (add UOA)

    for q in udeps:
        v=udeps[q]
        if v.get('uoa','')!='':
           setup['deps_'+q]=v['uoa']

    # Convert tags to string
    stags=''
    for q in tags:
        if q!='':
           if stags!='': stags+=','
           stags+=q.strip()

    # Check installation path
    pi=i.get('install_path','')
    ep=i.get('extra_path','')
    fp=i.get('full_path','')

    x=cus.get('input_path_example','')
    if x!='': pie=' (example: '+ye+')'
    else: pie=''

    if cs!=None and 'pre_path' in dir(cs):
       # Call customized script
       ii={"host_os_uoa":hosx,
           "host_os_uid":hos,
           "host_os_dict":hosd,
           "target_os_uoa":tosx,
           "target_os_uid":tos,
           "target_os_dict":tosd,
           "target_device_id":tdid,
           "cfg":d,
           "tags":tags,
           "env":env,
           "deps":udeps,
           "customize":cus,
           "self_cfg":cfg,
           "features":features,
           "version":ver,
           "ck_kernel":ck
          }

       if o=='con': ii['interactive']='yes'
       if i.get('quiet','')=='yes': ii['interactive']=''

       rx=cs.pre_path(ii)
       if rx['return']>0: return rx

       # Update install env from customized script (if needed)
       new_env=rx.get('install_env',{})
       if len(new_env)>0:
          pr_env.update(new_env)

    xprocess=True
    xsetup=True

    if i.get('skip_process','')=='yes': xprocess=False
    if i.get('skip_setup','')=='yes' or d.get('skip_setup','')=='yes': xsetup=False

    ps=d.get('process_script','')
    if pi=='':
       # Check if environment already exists to check installation path
       if enduoa=='':
          if o=='con':
             ck.out('')
             ck.out('Searching if CK environment for this package already exists using:')
             ck.out('  * Tags: '+stags)
             if len(udeps)>0:
                for q in udeps:
                    v=udeps[q]
                    ck.out('  * Dependency: '+q+'='+v.get('uoa',''))

          r=ck.access({'action':'search',
                       'module_uoa':cfg['module_deps']['env'],
                       'tags':stags,
                       'search_dict':{'setup':setup}})
          if r['return']>0: return r
          lst=r['lst']
          if len(lst)>0:
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
                if xprocess:
                   ck.out('')
                   ck.out('It appears that package is already installed or at least file from the package is already found in path: '+fp)

                   if ps!='':
                      ck.out('')
                      rx=ck.inp({'text':'Would you like to overwrite/process it again (y/N)? '})
                      x=rx['string'].strip().lower()
                      if x!='y' and x!='yes':
                         xprocess=False

                if xsetup:
                   ck.out('')
                   rx=ck.inp({'text':'Would you like to setup environment for this package again (Y/n)? '})
                   x=rx['string'].strip().lower()
                   if x=='n' or x=='no':
                      xsetup=False

             else:
                return {'return':1, 'error':'package is already installed in path '+pi}

       if enduoa=='' and iev=='yes':
          # Create dummy env and then set path there
          # TBD - if installation fails, we still have this dummy - need to check what to do ...
          #  can remove: ck rm env:* --tags=tmp
          xx=stags
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

          rz=prepare_install_path({})
          if rz['return']>0: return rz
          x=rz['path']

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

             # Tnen some extra path, if needed
             esp=cus.get('extra_suggested_path','')
             if esp!='':
                nm+=esp

             # Tnen some extra path, if needed
             if ep!='':
                nm+=esp

             # Finally OS
             if cus.get('no_os_in_suggested_path','')!='yes':
                nm+='-'+tosx

             pix=os.path.join(x, nm)
             if cus.get('no_os_in_suggested_path','')!='yes':
                if not tosx.endswith(tbits): pix+='-'+tbits

             if o=='con' and (i.get('ask','')=='yes' or cus.get('force_ask_path','')=='yes'):
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

       if edname!='':
          dname+=edname

       if cus.get('package_extra_name','')!='':
          dname+=cus['package_extra_name']

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
       ii={'action':'resolve',
           'module_uoa':cfg['module_deps']['env'],
           'host_os':hos,
           'target_os':tos,
           'target_device_id':tdid,
           'repo_uoa':enruoa,
           'install_to_env':iev,
           'deps':udeps}
       if o=='con': ii['out']='con'

       rx=ck.access(ii)
       if rx['return']>0: return rx
       sdeps=rx['bat']

    if o=='con' and pi!='':
       ck.out('')
       ck.out('Installation path: '+pi)
       ck.out('')

    if cs!=None and 'post_deps' in dir(cs):
       # Call customized script
       ii={"host_os_uoa":hosx,
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

       if o=='con': ii['interactive']='yes'
       if i.get('quiet','')=='yes': ii['interactive']=''

       rx=cs.post_deps(ii)
       if rx['return']>0: return rx

       # Update install env from customized script (if needed)
       new_env=rx.get('install_env',{})
       if len(new_env)>0:
          pr_env.update(new_env)

    soft_cfg={}

    # Check if continue processing
    if (ps!='' or (cs!=None and 'setup' in dir(cs))) and xprocess:
       # start bat
       sb=hosd.get('batch_prefix','')+'\n'

       if host_add_path_string!='':
          sb+=host_add_path_string+'\n\n'

       # Check if extra params to pass as environment
       param=i.get('param',None)
       params=d.get('params',{})
       params.update(i.get('params',{}))

       # Parse -D ...
       for k in i:
           if k.startswith('D'):
              params[k[1:]]=i[k]

       if param!=None:
          sb+='\n'
          xs=''
          if param.find(' ')>=0 and eifs!='': xs=eifs
          sb+=eset+' CK_PARAM='+xs+param+xs+'\n'

       if len(params)>0:
          for q in params:
              v=params[q]
              if v!=None:
                 xs=''
                 if v.find(' ')>=0 and eifs!='': xs=eifs
                 sb+=eset+' '+q+'='+xs+v+xs+'\n'

       sb+='\n'

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
       x=d.get('end_full_path',{}).get(tname2,'')
       fp=pi
       cont=True
       if x!='': 
          x=x.replace('$#sep#$', sdirs)
          x=x.replace('$#abi#$', tosd.get('abi',''))
          fp=os.path.join(fp,x)
          if os.path.isfile(fp):
             if o=='con':
                ck.out('')
                ck.out('It appears that package is already installed or at least file from the package is already found in path: '+fp)

                ck.out('')
                rx=ck.inp({'text':'Would you like to overwrite/process it again (y/N)? '})
                x=rx['string'].strip().lower()
                if x!='y' and x!='yes':
                   cont=False

       # Check if need to use scripts from another entry
       if cont:
          if cs!=None and 'setup' in dir(cs):
             # Call customized script
             ii={"host_os_uoa":hosx,
                 "host_os_uid":hos,
                 "host_os_dict":hosd,
                 "target_os_uoa":tosx,
                 "target_os_uid":tos,
                 "target_os_dict":tosd,
                 "target_device_id":tdid,
                 "cfg":d,
                 "tags":tags,
                 "env":env,
                 "deps":udeps,
                 "features":features,
                 "customize":cus,
                 "self_cfg":cfg,
                 "version":ver,
                 "ck_kernel":ck,
                 "path":ppp,
                 "script_path":ppp1,
                 "out":oo,
                 "install_path":pi
                }

             if o=='con': ii['interactive']='yes'
             if i.get('quiet','')=='yes': ii['interactive']=''

             rx=cs.setup(ii)
             if rx['return']>0: return rx

             soft_cfg=rx.get('soft_cfg',{})

             # Update install env from customized script (if needed)
             new_env=rx.get('install_env',{})
             if len(new_env)>0:
                pr_env.update(new_env)

          # Prepare process script
          if ps!='':
             ps+=sext
             px=os.path.join(ppp,ps)

             if not os.path.isfile(px):
                return {'return':1, 'error':'processing script '+ps+' is not found'}

             # Add deps if needed before running
             if sdeps!='':
                sb+=sdeps

             # Add compiler dep again, if there
             for k in sorted(udeps, key=lambda v: udeps[v].get('sort',0)):
                 if 'compiler' in k:
                    x=udeps[k].get('bat','').strip()
                    if x!='' and not sb.endswith(x):
                       sb+='\n'+x+' 1\n\n'

             # Add misc environment (prepared above)
             for q in pr_env:
                 qq=str(pr_env[q])

                 qq=qq.replace('$<<',svarb).replace('>>$',svare)

                 if qq.find(' ')>0:
                    qq=eifs+qq+eifs
                 sb+=eset+' '+q+'='+qq+'\n'

             # If install path has space, add quotes for some OS ...
             xs=''
             if pi.find(' ')>=0 and eifs!='': xs=eifs
             sb+=eset+' INSTALL_DIR='+xs+pi+xs+'\n'

             xs=''
             if p.find(' ')>=0 and eifs!='': xs=eifs
             sb+=eset+' PACKAGE_DIR='+xs+ppp+xs+'\n'

             xs=''
             if p.find(' ')>=0 and eifs!='': xs=eifs
             sb+=eset+' ORIGINAL_PACKAGE_DIR='+xs+p+xs+'\n'

             sb+='\n'

             xs=''
             if p.find(' ')>=0 and eifsc!='': xs=eifsc
             sb+=scall+' '+xs+px+xs+'\n\n'

             if wb=='yes' and d.get('check_exit_status','')!='yes':
                sb+='exit /b 0\n'

             rs=i.get('record_script','')

             # Generate tmp file (or use record script)
             if rs!='':
                fn=rs
                if fn==os.path.basename(fn):
                   fn=os.path.join(os.getcwd(),fn)
             else:
                rx=ck.gen_tmp_file({'prefix':'tmp-ck-', 'suffix':sext})
                if rx['return']>0: return rx
                fn=rx['file_name']

             # Write to tmp file
             rx=ck.save_text_file({'text_file':fn, 'string':sb})
             if rx['return']>0: return rx

             # Go to installation path
             if not os.path.isdir(pi):
                os.makedirs(pi)
             os.chdir(pi)

             # Check if need to set executable flags
             se=hosd.get('set_executable','')
             if se!='':
                x=se+' '+fn
                rx=os.system(x)

             # Run script
             rx=os.system(fn)

             # Remove script (if tmp)
             if rs=='' and os.path.isfile(fn): 
                os.remove(fn)

             if rx>0: 
                return {'return':1, 'error':'package installation failed'}

    # Preparing soft registration
    ii={'action':'setup',
        'module_uoa':cfg['module_deps']['soft'],
        'data_uoa':suoa,
        'soft_name':dname,
        'host_os':hos,
        'target_os':tos,
        'target_device_id':tdid,
        'tags':stags,
        'customize':cus,
        'features':features,
        'env_new':'yes',
        'env_repo_uoa':enruoa,
        'env_data_uoa':enduoa,
        'env':env,
        'extra_version':ev
       }

    nw='no'
    if enduoa=='': nw='yes'

    if cus.get('collect_device_info','')!='yes':
        ii['skip_device_info_collection']='yes'

    if d.get('remove_deps','')=='yes':
       ii['deps_copy']=udeps
    else:
       ii['deps']=udeps

    if d.get('no_install_path','')!='yes':
       if fp!='':
          ii['full_path']=fp
          ii['full_path_install']=pi
       elif pi!='':              # mainly for compatibility with previous CK soft manager
          ii['install_path']=pi

    if duid!='': ii['package_uoa']=duid

    if len(soft_cfg)>0:
       ii.update(soft_cfg)

    # Recording cus dict to install dir to be able to rebuild env later if needed 
    if pi!='':
       pic=os.path.join(pi, cfg['ck_install_file'])

       if o=='con':
          ck.out('')
          ck.out('Recording CK configuration to '+pic+' ...')

       rx=ck.save_json_to_file({'json_file':pic, 'dict':ii})
       if rx['return']>0: return rx

    # Check if need to setup environment
    if xsetup:
       if suoa=='':
          return {'return':1, 'error':'Software environment UOA is not defined in this package (soft_uoa)'}

#       if extra_dir!='':
#          pi+=sdirs+extra_dir

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

          if o=='con': ii['out']='con'

          rx=ck.access(ii)
          if rx['return']>0: return rx

          enduoa=rx['env_data_uoa']
          enduid=rx['env_data_uid']

    if o=='con' and pi!='':
       ck.out('')
       ck.out('Installation path: '+pi)
       ck.out('')

    elapsed_time=time.time()-start_time
    if o=='con':
       ck.out('Installation time: '+str(elapsed_time)+' sec.')

    return {'return':0, 'elapsed_time':elapsed_time, 'env_data_uoa':enduoa, 'env_data_uid':enduid}

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
        ii={'action':'install',
            'module_uoa':work['self_module_uid'],
            'tags':tags,
            'host_os':hos,
            'target_os':ntos,
            'device_id':tdid,
            'out':oo}
        r=ck.access(ii)
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
    ii=copy.deepcopy(i)

    ii['out']=''
    ii['action']='list'
    ii['add_meta']='yes'

    rx=ck.access(ii)
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

           ep=cus.get('env_prefix','')

           xhos=lm.get('only_for_host_os_tags',[])
           xtos=lm.get('only_for_target_os_tags',[])

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
              ck.out('Host OS tags: <i>'+yhos+'</i>')
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
