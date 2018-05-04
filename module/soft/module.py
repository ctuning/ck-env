#
# Collective Knowledge (checking and installing software)
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
env_install_path='CK_TOOLS'
env_search='CK_DIRS'

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
# detect is given software is already installed and register it in the CK or install it if package exists (the same as 'check')

def detect(i):
    """
    Input:  {
              (host_os)           - host OS (detect, if omitted)
              (target_os)         - target OS (detect, if omitted)
              (target_device_id)  - target device ID (detect, if omitted)

              (data_uoa) or (uoa) - software UOA entry
               or
              (tags)              - search UOA by tags (separated by comma)

              (interactive)       - if 'yes', and has questions, ask user
              (quiet)             - if 'yes', do not ask questions but select default value

              (skip_help)         - if 'yes', skip print help if not detected (when called from env setup)

              (deps)              - already resolved deps (if called from env)

              (extra_version)     - add extra version, when registering software 
                                    (for example, -trunk-20160421)

              (force_env_data_uoa) - force which env UID to use when regstering detect software -
                                     useful when reinstalling broken env entry to avoid breaking
                                     all dependencies of other software ...

              (search_dirs)        - extra directories where to search soft (string separated by comma)

              (soft_name)          - name to search explicitly

              (version_from)       - check version starting from ... (string or list of numbers)
              (version_to)         - check version up to ... (string list of numbers)

              (full_path)          - force full path (rather than searching in all directories)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              path_install - path to the detected software
              cus          - dict with filled in info for the software
            }

    """

    return check(i)

##############################################################################
# detect soft (internal function - gradually outdated)

def internal_detect(i):
    """
    Input:  {
              (host_os)           - host OS (detect, if omitted)
              (target_os)         - target OS (detect, if omitted)
              (target_device_id)  - target device ID (detect, if omitted)

              (data_uoa) or (uoa) - software UOA entry
               or
              (tags)              - search UOA by tags (separated by comma)

              (tool)              - force this tool name

              (env)               - if !='', use this env string before calling compiler (to set up env)

              (show)              - if 'yes', show output
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              version_str  - version as string
              version_lst  - version as list of strings
              version_raw  - raw list of strings (output of --version)
            }

    """

    import os

    o=i.get('out','')

    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')

    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'host_os':hos,
                 'target_os':tos,
                 'target_device_id':tdid,
                 'skip_info_collection':'yes'})
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    hplat=hosd['ck_name']
    tplat=tosd['ck_name']

    env=i.get('env','')

    ubtr=hosd.get('use_bash_to_run','')

    svarb=hosd.get('env_var_start','')
    svarb1=hosd.get('env_var_extra1','')
    svare=hosd.get('env_var_stop','')
    svare1=hosd.get('env_var_extra2','')
    sexe=hosd.get('set_executable','')
    sbp=hosd.get('bin_prefix','')
    envsep=hosd.get('env_separator','')
    scall=hosd.get('env_call','')
    sext=hosd.get('script_ext','')

    # Check soft UOA
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
       ck.out('Software description entry found: '+x)

    # Check if has custom script
    cs=None
    rx=ck.load_module_from_path({'path':p, 'module_code_name':cfg['custom_script_name'], 'skip_init':'yes'})
    if rx['return']==0: 
       cs=rx['code']

    # Checking name
    cus=d.get('customize',{})
    tool=i.get('tool','')
    if tool=='':
       if not skip and cus.get('soft_file_as_env','')!='':
          tool=svarb+cus['soft_file_as_env']+svare

       if cus.get('soft_file_not_tool','')!='yes':
          ry=prepare_target_name({'host_os_dict':hosd,
                                  'target_os_dict':tosd,
                                  'cus':cus})
          if ry['return']>0: return ry
          tool=ry['tool']

    # Preparing CMD
    soft_version_cmd=cus.get('soft_version_cmd',{}).get(hplat,'')

    if o=='con':
       ck.out('')
       ck.out('Prepared cmd: '+soft_version_cmd+' ...')

    # Check version (via customized script) ...
    ver=''
    lst=[]
    ii={'full_path':tool,
        'bat':env,
        'host_os_dict':hosd,
        'target_os_dict':tosd,
        'cmd':soft_version_cmd,
        'use_locale':cus.get('use_locale_for_version',''),
        'custom_script_obj':cs}
    rx=get_version(ii)
    if rx['return']==0:
       ver=rx['version']
       lst=rx['version_lst']

    if ver=='':
       return {'return':16, 'error':'version was not detected'}

    # Split version
    rx=split_version({'version':ver})
    if rx['return']>0: return rx
    sver=rx['version_split']

    if i.get('show','')=='yes':
       ck.out('Output:')
       ck.out('')
       for q in lst:
           ck.out('  '+q)

    if o=='con':
       ck.out('')
       ck.out('Version detected: '+ver)

    return {'return':0, 'version_str':ver, 
                        'version_lst':sver, 
                        'version_raw':lst}

##############################################################################
# setup environment for a given software - 
# it is a low level routine which ask you the exact path to the tool and its version

def setup(i):
    """
    Input:  {
              (host_os)           - host OS (detect, if omitted)
              (target_os)         - target OS (detect, if omitted)
              (target_device_id)  - target device ID (detect, if omitted)

              (data_uoa) or (uoa) - soft configuration UOA
               or
              (tags)              - search UOA by tags (separated by comma)

              (soft_name)         - use this user friendly name for environment entry
              (soft_add_name)     - add extra name to above name (such as anaconda)

              (customize)         - dict with custom parameters 
                                    (usually passed to customize script)

                                    skip_add_dirs
                                    skip_add_to_path
                                    skip_add_to_bin
                                    skip_add_to_ld_path
                                    add_include_path

                                    skip_path - skiping installation path (for local versions)

                                    version      - add this version
                                    skip_version - if 'yes', do not add version

              (skip_path)         - skiping installation path (for local versions)

              (env)               - update default env with this dict

              (deps)              - list with dependencies (in special format, possibly resolved (from package))

              (install_path)      - path with soft is installed
              (full_path)         - full path to a tool or library (install_path will be calculated automatically)

              (bat_file)          - if !='', record environment to this bat file, 
                                    instead of creating env entry

              (quiet)             - if 'yes', minimize questions

              (env_data_uoa)      - use this data UOA to record (new) env
              (env_repo_uoa)      - use this repo to record new env
              (env_new)           - if 'yes', do not search for environment (was already done in package, for example)

              (package_uoa)       - if called from package, record package_uoa just in case

              (reset_env)         - if 'yes', do not use environment from existing entry, but use original one

              (extra_version)     - add extra version, when registering software 
                                    (for example, -trunk-20160421)

              (skip_device_info_collection) - if 'yes', do not collect device info
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              env_data_uoa - environment entry UOA
              env_data_uid - environment entry UID

              deps         - resolved dependencies (if any)
            }

    """

    import os
    import json

    o=i.get('out','')

    env_new=i.get('env_new','')

    ########################################################################
    # Check host/target OS/CPU
    hos=i.get('host_os','')
    tos=i.get('target_os','')
    tdid=i.get('target_device_id','')
    if tdid=='': tdid=i.get('device_id','')

    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform.os'],
        'host_os':hos,
        'target_os':tos,
        'target_device_id':tdid,
        'skip_info_collection':'no'}

    if i.get('skip_device_info_collection','')=='yes':
        ii['skip_info_collection']='yes'

    r=ck.access(ii)
    if r['return']>0: return r

    features=r.get('features',{})

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    tbits=tosd.get('bits','')

    hplat=hosd['ck_name']
    tplat=tosd['ck_name']

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

    # Check soft UOA
    duoa=i.get('uoa','')
    if duoa=='': duoa=i.get('data_uoa','')

    tags=i.get('tags','')

    if duoa=='':
       xcids=i.get('xcids',[])
       if len(xcids)>0:
          duoa=xcids[0].get('data_uoa','')

    duid=duoa

    if duoa=='' and tags!='':
       r=ck.access({'action':'search',
                    'module_uoa':work['self_module_uid'],
                    'tags':tags})
       if r['return']>0: return r
       l=r['lst']
       if len(l)>0:
          duid=l[0].get('data_uid')
          duoa=duid

    d={}
    p=''

    ########################################################################
    if duoa=='':
       # Try to detect CID in current path
       rx=ck.detect_cid_in_current_path({})
       if rx['return']==0:
          duoa=rx.get('data_uoa','')

    if duoa!='':
       # Load defined or found soft entry
       r=ck.access({'action':'load',
                    'module_uoa':work['self_module_uid'],
                    'data_uoa':duoa})
       if r['return']>0: return r

       d=r['dict']
       p=r['path']

       duoa=r['data_uoa']
       duid=r['data_uid']

    if duoa=='':
       try:
           p=os.getcwd()
       except OSError:
           os.chdir('..')
           p=os.getcwd()

       pc=os.path.join(p, ck.cfg['subdir_ck_ext'], ck.cfg['file_meta'])

       found=False
       if os.path.isfile(pc):
          r=ck.load_json_file({'json_file':pc})
          if r['return']==0:
             d=r['dict']
             found=True

       if not found:
          return {'return':1, 'error':'software UOA (data_uoa) is not defined'}

    if o=='con':
       if duoa!='' and duid!='':
          x=': '+duoa
          if duid!=duoa: x+=' ('+duid+')'
       else:
          x=' in local directory'
       ck.out('  Software entry found'+x)

    # Check deps, customize, install path
    ltags=d.get('tags',[])
    deps=d.get('deps',{})
    env=d.get('env',{})
    cus=d.get('customize',{})
    pi=''
    envp=cus.get('env_prefix','')
    envps=envp+'_SET'

    san=i.get('soft_add_name','')

    dname=d.get('soft_name','')
    if i.get('soft_name','')!='': 
       dname=i['soft_name']
    else:
       if cus.get('package_extra_name','')!='':
          dname+=cus['package_extra_name']
    if san!='':
       dname+=san

    csp=d.get('can_skip_path','')

    ev=i.get('extra_version','')
    if ev=='':
       ev=cus.get('extra_version','')

    # Add tags from the search!
    for q in tags.split(','):
        q1=q.strip()
        if q1!='' and q1 not in ltags: ltags.append(q1)

    # Finish tags
    tg='host-os-'+hosx
    if tg not in ltags: ltags.append(tg)

    tg='target-os-'+tosx
    if tg not in ltags: ltags.append(tg)

    tg=tbits+'bits'
    if tg not in ltags: ltags.append(tg)

    ########################################################################
    # Check if environment already set (preload to update)
    enduoa=i.get('env_data_uoa','')
    enruoa=i.get('env_repo_uoa','')
    update=False

    if enduoa!='':
       rx=ck.access({'action':'load',
                     'module_uoa':cfg['module_deps']['env'],
                     'data_uoa':enduoa,
                     'repo_uoa':enruoa})
       if rx['return']==0:
          update=True

          edx=rx['dict']

          cus.update(edx.get('customize',{}))
          deps=edx.get('deps',{})
          if i.get('reset_env','')!='yes' and 'tmp' not in edx.get('tags',[]):
             env=edx.get('env',{})
          pi=cus.get('path_install','')

    # Update from input
    udeps=i.get('deps',{})
    deps.update(udeps)

    uenv=i.get('env',{})
    env.update(uenv)

    ucus=i.get('customize',{})
    cus.update(ucus)

    pi1=i.get('install_path','')
    if pi1!='': pi=pi1

    fp=i.get('full_path','')

    ########################################################################
    # Check meta
    setup={'host_os_uoa':hos,
           'target_os_uoa':tos,
           'target_os_bits':tbits}

    # Resolve deps (if not ignored, such as when installing local version with all dependencies set)
    if cus.get('ignore_deps','')=='yes':
       deps={}

    sdeps=''
    sdeps1=''
    if len(deps)>0:
       ii={'action':'resolve',
           'module_uoa':cfg['module_deps']['env'],
           'host_os':hos,
           'target_os':tos,
           'target_device_id':tdid,
           'repo_uoa':enruoa,
           'deps':deps}
       if o=='con': ii['out']='con'

       rx=ck.access(ii)
       if rx['return']>0: return rx
       sdeps=rx['bat']
       sdeps1=rx['cut_bat']
       deps=rx['deps'] # Update deps (add UOA)

    for q in deps:
        v=deps[q]
        vuoa=v.get('uoa','') # can be undefined if OS specific
        if vuoa!='': setup['deps_'+q]=vuoa

    # Check if has custom script
    cs=None
    rx=ck.load_module_from_path({'path':p, 'module_code_name':cfg['custom_script_name'], 'skip_init':'yes'})
    if rx['return']==0: 
       cs=rx['code']

    ########################################################################
    ########################################################################
    ########################################################################
    ########################################################################
    # Starting processing soft

    # Check via full path first
    if pi=='' and fp=='' and o=='con' and cus.get('skip_path','')!='yes' and i.get('skip_path','')!='yes' and not update:
       ck.out('')

       ry=prepare_target_name({'host_os_dict':hosd,
                               'target_os_dict':tosd,
                               'cus':cus})
       if ry['return']>0: return ry
       sname=ry['tool']

       y0='installed library, tool or script'
       if sname!='': 
          suname=d.get('soft_name','')

          if cus.get('skip_soft_file_is_asked','')=='yes':
             if suname!='': y0=suname
          else:  
             y0=sname
             if suname!='': y0=suname+' ('+sname+')'

       y1='full path to '+y0

       y2=''
       y3=cus.get('soft_path_example',{}).get(hplat,'')
       if y3!='': y2=' (example: '+y3+')'

       r=ck.inp({'text':'Enter '+y1+y2+': '})
       fp=r['string'].strip()

    # Check if file really exists and check version if a tool
    ver=cus.get('version','')
    vercus=ver
    if fp!='':
       if cus.get('skip_file_check','')!='yes' and not os.path.isfile(fp):
          return {'return':1, 'error':'software not found in a specified path ('+fp+')'}

       skip_existing='no'
       if cus.get('force_cmd_version_detection','')=='yes':
          skip_existing='yes'
          ver=''

       if ver=='':
          soft_version_cmd=cus.get('soft_version_cmd',{}).get(hplat,'')

          if o=='con':
             ck.out('')
             ck.out('  Attempting to detect version automatically (if supported) ...')

          # Check version (via customized script) ...
          ii={'full_path':fp,
              'bat':sdeps,
              'host_os_dict':hosd,
              'target_os_dict':tosd,
              'cmd':soft_version_cmd,
              'custom_script_obj':cs,
              'skip_existing':skip_existing,
              'skip_add_target_file':cus.get('soft_version_skip_add_target_file',''),
              'use_locale':cus.get('use_locale_for_version','')}
          rx=get_version(ii)
          if rx['return']>0 and rx['return']!=16 and rx['return']!=22: return rx
          if rx['return']==0:
             ver=rx['version']
             if o=='con':
                ck.out('')
                ck.out('  Detected version: '+ver)
          else:
             if o=='con':
                ck.out('')
                ck.out('  WARNING: didn\'t manage to automatically detect software version!')

    ########################################################################
    # Get various git info ...
    ss1=''
    ss2=''
    ss3=''
    ss4=''
    ss5=''

    ver_to_search=ver

    if cus.get('use_git_revision','')=='yes':
       import datetime

       psrc=cus.get('git_src_dir','')

       dfp=i.get('full_path_install','')

       if dfp!='':
          if psrc!='':
             dfp=os.path.join(dfp, psrc)

          try:
              pwd1=os.getcwd()
          except OSError:
              os.chdir('..')
              pwd1=os.getcwd()

          if os.path.isdir(dfp):
             os.chdir(dfp)

             r=ck.access({'action':'run_and_get_stdout',
                          'module_uoa':cfg['module_deps']['os'],
                          'cmd':['git','rev-parse','--short','HEAD']})
             if r['return']==0 and r['return_code']==0: 
                ss1=r['stdout'].strip()

             r=ck.access({'action':'run_and_get_stdout',
                          'module_uoa':cfg['module_deps']['os'],
                          'cmd':['git','log','-1','--format=%cd']})
             if r['return']==0 and r['return_code']==0: 
                ss2=r['stdout'].strip()
                if ss2!='':
                   ss2x=ss2
                   j=ss2x.find(' +')
                   if j<0:
                      j=ss2x.find(' -')
                   if j>0:
                      ss2x=ss2[:j]

                   x=datetime.datetime.strptime(ss2x, '%a %b %d %H:%M:%S %Y')

                   ss3=x.isoformat()

                   ss4=ss3[:10].replace('-','')

                   if ss1!='':
                      ss5=ss4+'-'+ss1

             if 'git_info' not in cus:
                cus['git_info']={}

             cus['git_info']['revision']=ss1
             cus['git_info']['datetime']=ss2
             cus['git_info']['iso_datetime']=ss3
             cus['git_info']['iso_datetime_cut']=ss4
             cus['git_info']['iso_datetime_cut_revision']=ss5

             if o=='con':
                ck.out('')
                if ss1!='':
                   ck.out('Detected GIT revision:                 '+ss1)
                if ss2!='':
                   ck.out('Detected GIT date time of last commit: '+ss2)

             os.chdir(pwd1)

             ver+='-'+ss1

    ########################################################################
    # Ask for version if was not detected or is not explicitly specified (for example, from a package)
    if ver==''  and cus.get('skip_version','')!='yes' and o=='con':
       ck.out('')
       r=ck.inp({'text':'Enter version of this software (for example, 3.21.6-2 or press Enter if default/unknown): '})
       ver=r['string'].strip().lower()
       ver_to_search=ver

    # Add extra, if needed (useful for changing trunks)
    if ev!='':
       ver+=ev
       ver_to_search+=ev

    # If cutomized version has changed, try to check env again ...
    if vercus!=ver:
       env_new='no'

    # Split version
    rx=split_version({'version':ver})
    if rx['return']>0: return rx
    sver=rx['version_split']

    # Add version to setup and separate into tags
    setup['version']=ver_to_search
    setup['version_split']=sver

    # Prepare tags from version
    if ver!='': 
       x=''
       for q in sver:
           if x!='':x+='.'
           x+=str(q)

           tg='v'+x

           if tg not in ltags:
              ltags.append(tg)

    # Prepare final tags string
    stags=''
    for q in ltags:
        if q!='':
           if stags!='': stags+=','
           stags+=q.strip()

    ########################################################################
    # Search if environment is already registered for this version
    # (to delete or reuse it)
    finish=False
    if enduoa=='' and env_new!='yes':
       if o=='con':
          ck.out('')
          ck.out('Searching if environment already exists using:')
          ck.out('  * Tags: '+stags)
          if len(deps)>0:
             for q in deps:
                 v=deps[q]
                 vuoa=v.get('uoa','')
                 if vuoa!='':
                    ck.out('  * Dependency: '+q+'='+v.get('uoa',''))

       r=ck.access({'action':'search',
                    'module_uoa':cfg['module_deps']['env'],
                    'repo_uoa':enruoa,
                    'tags':stags,
                    'search_dict':{'setup':setup}})
       if r['return']>0: return r
       lst=r['lst']

       if len(lst)>0:
          fe=lst[0]

          enduoa=fe['data_uoa']
          enduid=fe['data_uid']

          if o=='con':
             x=enduoa
             if enduid!=enduoa: x+=' ('+enduid+')'

             ck.out('')
             ck.out('Environment already registered for this version: '+x)

             update=False
             if i.get('update','')=='yes':
                update=True

             if not update:
                if o=='con':
                   ck.out('')
                   r=ck.inp({'text':'Would you like to delete this entry and re-register environment (Y/n): '})
                   dl=r['string'].strip().lower()

                   if dl=='' or dl=='y' or dl=='yes':
                      update=False

                      rx=ck.access({'action':'delete',
                                    'module_uoa':cfg['module_deps']['env'],
                                    'data_uoa':enduoa,
                                    'repo_uoa':enruoa})
                      if rx['return']>0: return rx

                   else:
                      ck.out('')
                      r=ck.inp({'text':'Would you like to update this entry (Y/n): '})
                      upd=r['string'].strip().lower()

                      if upd=='' or upd=='y' or upd=='yes':
                         update=True
                      else:
                         finish=True

             if update:
                rx=ck.access({'action':'load',
                              'module_uoa':cfg['module_deps']['env'],
                              'data_uoa':enduoa,
                              'repo_uoa':enruoa})
                if rx['return']>0: return rx

                edx=rx['dict']

                cus1=edx.get('customize',{})
                deps1=edx.get('deps',{})
                env1=edx.get('env',{})

                cus.update(cus1)
                deps.update(deps1)
                env.update(env1)

                pi=cus.get('path_install','')

       else:
          if o=='con':
             ck.out('')
             ck.out('    Environment with above tags is not yet registered in CK ...')

    ############################################################
    if not finish:
       # Prepare environment and batch
       sb=''

       if o=='out':
          ck.out('')
          ck.out('Preparing environment and batch file ...')

       sdirs=hosd.get('dir_sep','')

       wb=tosd.get('windows_base','')

       rem=hosd.get('rem','')
       eset=hosd.get('env_set','')
       svarb=hosd.get('env_var_start','')
       svare=hosd.get('env_var_stop','')
       sdirs=hosd.get('dir_sep','')
       evs=hosd.get('env_var_separator','')
       eifs=hosd.get('env_quotes_if_space','')

       ellp=hosd.get('env_ld_library_path','')
       if ellp=='': ellp='LD_LIBRARY_PATH'
       elp=hosd.get('env_library_path','')
       if elp=='': elp='LIBRARY_PATH'

       # Check installation path
       if fp=='' and cus.get('skip_path','')!='yes' and i.get('skip_path','')!='yes' and not update:
          if o=='con':
#             if update:
#                ck.out('')
#                ck.out('Current path to installed tool: '+pi)
#                r=ck.inp({'text':'Input new path to installed tool or press Enter to keep old: '})
#                pix=r['string'].strip()
#                if pix!='': pi=pix
             if pi=='':
                ck.out('')

                ye=cus.get('input_path_example','')
                if ye!='': y=' (example: '+ye+')'
                else: y=''

                y1=cus.get('input_path_text','')
                if y1=='': y1='path to installed software (root directory possibly pointing to bin, lib, include, etc)'
 
                r=ck.inp({'text':'Enter '+y1+y+': '})
                pi=r['string'].strip().strip('"')

                ipr=cus.get('input_path_remove','')
                if ipr!='' and ipr>0:
                   for q in range(0,ipr):
                       try:
                          pi=os.path.split(pi)[0]
                       except:
                          pass

          if pi=='' and csp!='yes':
             return {'return':1, 'error':'installation path is not specified'}

       if fp!='':
          cus['full_path']=fp

       if pi!='':
          cus['path_install']=pi

       ### OLD start
       if cus.get('skip_add_dirs','')!='yes' and pi!='':
          if cus.get('add_include_path','')=='yes' and cus.get('path_include','')=='':
             pii=pi+sdirs+'include'
             cus['path_include']=pii

          if cus.get('skip_add_to_bin','')!='yes':
             pib=pi
             if cus.get('skip_add_bin_ext','')!='yes': pib+=sdirs+'bin'
             cus['path_bin']=pib

          if cus.get('skip_add_to_ld_path','')!='yes' and cus.get('path_lib','')=='':
             plib=pi+sdirs+'lib64'
             if not os.path.isdir(plib):
                plib=pi+sdirs+'lib32'
                if not os.path.isdir(plib):
                   plib=pi+sdirs+'lib' 
                   if not os.path.isdir(plib):
                      return {'return':1, 'error':'can\'t find lib path'}
             cus['path_lib']=plib
       else:
          cus['skip_path']='yes'
       ### OLD stop

       # If install path has space, add quotes for some OS ...
       xs=''
       if pi.find(' ')>=0 and eifs!='':
          xs=eifs

       # Check if has custom script
       cs=None
       rx=ck.load_module_from_path({'path':p, 'module_code_name':cfg['custom_script_name'], 'skip_init':'yes'})
       if rx['return']==0: 
          cs=rx['code']

       sadd=''
       if cs!=None and 'setup' in dir(cs):
          # Prepare info
          rx=ck.gen_tmp_file({})
          if rx['return']>0: return rx
          fn=rx['file_name']

          # Call setup script
          ii={"host_os_uoa":hosx,
              "host_os_uid":hos,
              "host_os_dict":hosd,
              "target_os_uoa":tosx,
              "target_os_uid":tos,
              "target_os_dict":tosd,
              "target_device_id":tdid,
              "soft_uoa":duoa,
              "soft_name":dname,
              "tags":ltags,
              "cfg":d,
              "env":env,
              "deps":deps,
              "deps_copy":i.get('deps_copy',{}),
              "customize":cus,
              "self_cfg":cfg,
              "version":ver,
              "version_split":sver,
              "features":features,
              "ck_kernel":ck
             }

          if o=='con': ii['interactive']='yes'
          if i.get('quiet','')=='yes': ii['interactive']=''

          rx=cs.setup(ii)
          if rx['return']>0: return rx

          sadd=rx['bat']
          pi=cus.get('path_install','')

          if cus.get('soft_name','')!='':
              dname=cus['soft_name']

          if cus.get('soft_extra_name','')!='':
              dname+=cus['soft_extra_name']

       #########################################################
       # Finish batch
       sb+=hosd.get('batch_prefix','')+'\n'

       check_if_set=hosd.get('batch_check_if_set','')
       if check_if_set!='':
          sb+=check_if_set.replace('$#ck_var#$',envps)+'\n'

       x=duoa
       if duid!=duoa: x+=' ('+duid+') '
       if len(tags)>0:
          y=''
          for q in ltags:
              if y!='': y+=','
              y+=q
          x+=' ('+y+')'
       sb+=rem+' '+'Soft UOA           = '+x+'\n'

       sb+=rem+' '+'Host OS UOA        = '+hosx+' ('+hos+')\n'
       sb+=rem+' '+'Target OS UOA      = '+tosx+' ('+tos+')\n'
       sb+=rem+' '+'Target OS bits     = '+tbits+'\n'
       if ver!='':
          sb+=rem+' '+'Tool version       = '+ver+'\n'
          cus['version']=ver
       if len(sver)>0:
          sb+=rem+' '+'Tool split version = '+json.dumps(sver)+'\n'
          cus['version_split']=sver
       sb+='\n'

       if sdeps!='':
          sb+=rem+' Dependencies:\n'
          sb+=sdeps1+'\n'

       if cus.get('skip_path','')!='yes' and i.get('skip_path','')!='yes' and pi!='':
          sb+=eset+' '+envp+'='+xs+pi+xs+'\n'
          cus['path_install']=pi

       envp_b=envp+'_BIN'
       pib=cus.get('path_bin','')
       envp_l=envp+'_LIB'
       plib=cus.get('path_lib','')
       envp_i=envp+'_INCLUDE'
       piib=cus.get('path_include','')

       if cus.get('skip_add_dirs','')!='yes': # and pi!='':
          if pib!='' and cus.get('skip_add_to_bin','')!='yes': sb+=eset+' '+envp_b+'='+xs+pib+xs+'\n'
          if plib!='': sb+=eset+' '+envp_l+'='+xs+plib+xs+'\n'
          if piib!='': sb+=eset+' '+envp_i+'='+xs+piib+xs+'\n'

       if sadd!='':
          sb+='\n'+sadd

       # Add all env
       for k in sorted(env):
           v=str(env[k])

           if eifs!='' and wb!='yes':
              if v.find(' ')>=0 and not v.startswith(eifs):
                 v=eifs+v+eifs

           sb+=eset+' '+k+'='+v+'\n'
       sb+='\n'

       # Add to existing vars
       if cus.get('add_to_path','')=='yes' or (cus.get('skip_add_to_path','')!='yes' and cus.get('skip_add_to_bin','')!='yes' and cus.get('skip_dirs','')!='yes' and pi!=''):
          sb+=eset+' PATH='+svarb+envp_b+svare+evs+svarb+'PATH'+svare+'\n'

       if pi!='' and cus.get('skip_add_to_ld_path','')!='yes' and cus.get('skip_dirs','')!='yes':
          sb+=eset+' '+elp+'='+svarb+envp_l+svare+evs+svarb+elp+svare+'\n'
          sb+=eset+' '+ellp+'='+svarb+envp_l+svare+evs+svarb+ellp+svare+'\n'

       # Say that environment is set (to avoid recursion)
       sb+=eset+' '+envps+'=1\n'

       # Finish environment batch file
       if wb=='yes':
          sb+='\n'
          sb+='exit /b 0\n'

       # Check if save to bat file *****************************************************************************************
       bf=i.get('bat_file', '')
       pnew=''

       if bf=='':
          bf=cfg['default_bat_name']+hosd.get('script_ext','')

          # Preparing to add or update entry
          xx='added'

          ltags=sorted(ltags)

          dd={'tags':ltags,
              'setup':setup,
              'env':env,
              'deps':deps,
              'soft_uoa':duid,
              'customize':cus,
              'env_script':bf}

          if duid!='':
             dd['soft_uoa']=duid

          pduoa=i.get('package_uoa','')
          if pduoa!='':
             dd['package_uoa']=pduoa

          ii={'action':'add',
              'module_uoa':cfg['module_deps']['env'],
              'dict':dd,
              'sort_keys':'yes',
              'substitute':'yes'}

          if enduoa!='': ii['data_uoa']=enduoa
          if enruoa!='': ii['repo_uoa']=enruoa

          if update:
             ii['action']='update'
             xx='updated'

          # Adding/updating
          if dname!='':
             ii['data_name']=dname

          rx=ck.access(ii)
          if rx['return']>0: return rx

          enduoa=rx['data_uoa']
          enduid=rx['data_uid']

          pnew=rx['path']

          if o=='con':
             ck.out('')
             ck.out('Environment entry '+xx+' ('+enduoa+')!')

       # Record batch file
       if pnew=='': pb=bf
       else:        pb=os.path.join(pnew, bf)

       # Write file
       rx=ck.save_text_file({'text_file':pb, 'string':sb})
       if rx['return']>0: return rx

    return {'return':0, 'env_data_uoa':enduoa, 'env_data_uid':enduid, 'deps':deps}

##############################################################################
# search tool in pre-defined paths

def search_tool(i):
    """
    Input:  {
              path_list             - path list
              file_name             - name of file to find (can be with patterns)
              (recursion_level_max) - if >0, limit dir recursion
              (can_be_dir)          - if 'yes', return directory as well
              (return_symlinks)     - if 'yes', symlinks are returned as-is. Otherwise, they're resolved
            }

    Output: {
              return       - return code =  0, if successful
                                            >  0, if error
              (error)      - error text if return > 0

              list         - list of file (see ck.list_all_files)
              elapsed_time - elapsed time

            }
    """

    o=i.get('out','')

    import time
    import os
    start_time = time.time()

    pl=i['path_list']
    fn=i['file_name']
    pt=''

    rlm=i.get('recursion_level_max',0)
    cbd=i.get('can_be_dir','')
    return_symlinks = i.get('return_symlinks','')

    if fn.find('?')>=0 or fn.find('*')>=0:
       pt=fn
       fn=''

    lst=[]

    for p in pl:
        if o=='con':
           ck.out('    * Searching in '+p+' ...')

        r=list_all_files({'path':p, 
                          'file_name':fn, 
                          'pattern':pt,
                          'recursion_level_max':rlm})
        if r['return']>0: return r
        for q in r['list']:
            new=True
            if cbd!='yes' and os.path.isdir(q):
               new=False

#            if new:
#               for qq in lst:
#                   if os.path.realpath(q)==os.path.realpath(qq):
#                      new=False
#                      break

            if new:
               lst.append(q)

#    if return_symlinks != 'yes':
#      # resolving symlinks
#      lst = [os.path.realpath(p) for p in lst]
#      #removing duplicates
#      recorded_paths = set()
#      record_path = recorded_paths.add
#      lst = [p for p in lst if not (p in recorded_paths or record_path(p))]

    elapsed_time = time.time() - start_time

    return {'return':0, 'list':lst, 'elapsed_time':elapsed_time}


##############################################################################
# List all files recursively in a given directory

def list_all_files(i):
    """
    Input:  {
              path                  - top level path
              (file_name)           - search for a specific file name
              (pattern)             - return only files with this pattern
              (path_ext)            - path extension (needed for recursion)
              (recursion_level_max) - if >0, limit dir recursion
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              list         - list of found files
            }
    """

    import sys
    import os

    a=[]

    fname=i.get('file_name','')

    fname_with_sep=False
    if fname.find(os.sep)>=0:
        fname_with_sep=True

    pattern=i.get('pattern','')
    if pattern!='':
       import fnmatch

    pe=''
    if i.get('path_ext','')!='': 
       pe=i['path_ext']

    po=i.get('path','')
    if sys.version_info[0]<3: po=unicode(po)

    rl=i.get('recursion_level',0)
    rlm=i.get('recursion_level_max',0)

    if rlm>0 and rl>rlm: 
       return {'return':0, 'list':[]}

    try:
       dirList=os.listdir(po)
    except Exception as e:
       None
    else:
       for fn in dirList:
           p=''
           try:
              p=os.path.join(po, fn)
           except Exception as e: 
              pass

           if p!='':
              add=True

              if fname!='':
                  if fname_with_sep and os.path.isdir(p):
                      px=os.path.join(po,fname)
                      add=False
                      if os.path.isfile(px):
                          if px not in a:
                              a.append(px)

                  elif fname!=fn:
                      add=False

              if pattern!='' and not fnmatch.fnmatch(fn, pattern):
                 add=False

              if add:
                 a.append(p)

              recursive=False
              problem=False    # Need this complex structure to support UTF-8 file names in Python 2.7
              try:
                 if os.path.isdir(p): # and os.path.realpath(p)==p: # real path was useful
                                                                    # to avoid cases when directory links to itself
                                                                    # however, since we limit recursion, it doesn't matter ...
                    recursive=True
              except Exception as e: 
                 problem=True
                 pass

              if problem:
                 problem=False
                 try:
                    p=p.encode('utf-8')
                    if os.path.isdir(p): 
                       recursive=True
                 except Exception as e: 
                    problem=True
                    pass


                 if problem:
                    try:
                       p=p.encode(sys.stdin.encoding)
                       if os.path.isdir(p):
                          recursive=True
                    except Exception as e: 
                       pass

              if recursive:
                 r=list_all_files({'path':p, 'path_ext':os.path.join(pe, fn),
                                   'pattern':pattern, 'file_name':fname, 
                                   'recursion_level':rl+1, 'recursion_level_max':rlm})
                 if r['return']>0: return r
                 for q in r.get('list',[]):
                     a.append(q)

    return {'return':0, 'list':a}

##############################################################################
# check is given software is already installed and register it in the CK or install it if package exists (the same as 'detect')

def check(i):
    """
    Input:  {
              (target)            - if specified, use info from 'machine' module
                 or
              (host_os)           - host OS (detect, if omitted)
              (target_os)         - target OS (detect, if omitted)
              (target_device_id)  - target device ID (detect, if omitted)

              (data_uoa) or (uoa) - software UOA entry
               or
              (tags)              - search UOA by tags (separated by comma)

              (interactive)       - if 'yes', and has questions, ask user
              (quiet)             - if 'yes', do not ask questions but select default value

              (skip_help)         - if 'yes', skip print help if not detected (when called from env setup)

              (deps)              - already resolved deps (if called from env)

              (extra_version)     - add extra version, when registering software 
                                    (for example, -trunk-20160421)
                                    Be careful - if there is auto version detection,
                                    CK will say that version has changed and will try to remove entry!

              (extra_tags)         - add extra tags to separate created entry from others 
                                     (for example Python 2.7 vs Anaconda Python 2.7)

              (extra_name)         - add extra name to soft (such as anaconda)

              (force_env_data_uoa) - force which env UID to use when regstering detect software -
                                     useful when reinstalling broken env entry to avoid breaking
                                     all dependencies of other software ...

              (search_dirs)        - extra directories where to search soft (string separated by comma)

              (soft_name)          - name to search explicitly

              (version_from)       - check version starting from ... (string or list of numbers)
              (version_to)         - check version up to ... (string list of numbers)

              (full_path)          - force full path (rather than searching in all directories)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              path_install - path to the detected software
              cus          - dict with filled in info for the software
            }

    """

    import os
    import json
    import copy

    o=i.get('out','')
    oo=''
    if o=='con': oo=o

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
                 'target_device_id':tdid,
                 'skip_info_collection':'yes'})
    if r['return']>0: return r

    hos=r['host_os_uid']
    hosx=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']

    tosd.update(device_cfg.get('update_target_os_dict',{}))

    tbits=tosd.get('bits','')

    hplat=hosd.get('ck_name','')
    tplat=tosd.get('ck_name','')

    # Check versions
    vfrom=i.get('version_from',[])
    vto=i.get('version_to',[])

    if type(vfrom)!=list:
       rx=split_version({'version':vfrom})
       if rx['return']>0: return rx
       vfrom=rx['version_split']

    if type(vto)!=list:
       rx=split_version({'version':vto})
       if rx['return']>0: return rx
       vto=rx['version_split']

    # Check soft UOA
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

    cus=d.get('customize',{})

    duoa=r['data_uoa']
    duid=r['data_uid']

    ev=i.get('extra_version','')
    if ev=='':
       ev=cus.get('extra_version','')

    ########################################################################
    # Check env from input
    envx=copy.deepcopy(i.get('env',{}))
    for q in i:
        if q.startswith('env.'):
           envx[q[4:]]=i[q]

    # Check if restricts dependency to a given host or target OS
    rx=check_target({'dict':cus,
                     'host_os_uoa':hosx,
                     'host_os_dict':hosd,
                     'target_os_uoa':tosx,
                     'target_os_dict':tosd})
    if rx['return']>0: return rx

    # Check if need to resolve dependencies
    deps=i.get('deps',{})
    sbat=''
    if len(deps)==0:
       deps=d.get('deps',{})

       if len(deps)>0:
          ii={'action':'resolve',
              'module_uoa':cfg['module_deps']['env'],
              'host_os':hos,
              'target_os':tos,
              'target_device_id':tdid,
              'deps':deps,
#              'env':envx,
              'env':copy.deepcopy(envx),
              'out':oo}
          rx=ck.access(ii)
          if rx['return']>0: return rx

          sbat=rx['bat']

#    if o=='con':
#       x=duoa
#       if duid!=duoa: x+=' ('+duid+')'
#       ck.out('Software description entry found: '+x)

    rr={'return':0}

    # Check if has custom script
    cs=None
    rx=ck.load_module_from_path({'path':p, 'module_code_name':cfg['custom_script_name'], 'skip_init':'yes'})
    if rx['return']==0: 
       cs=rx['code']

    soft_version_cmd=cus.get('soft_version_cmd',{}).get(hplat,'')

    # Check where to search depending if Windows or Linux
    dirs=[]
    if hplat=='win':
       x=os.environ.get('ProgramW6432','')
       if x!='' and os.path.isdir(x) and x not in dirs:
          dirs.append(x)
       x=os.environ.get('ProgramFiles(x86)','')
       if x!='' and os.path.isdir(x) and x not in dirs:
          dirs.append(x)
       x=os.environ.get('ProgramFiles','')
       if x!='' and os.path.isdir(x) and x not in dirs:
          dirs.append(x)
       x='C:\\Program Files'
       if os.path.isdir(x) and x not in dirs:
          dirs.append(x)
       x='D:\\Program Files'
       if os.path.isdir(x) and x not in dirs:
          dirs.append(x)
       x='C:\\Program Files (x86)'
       if os.path.isdir(x) and x not in dirs:
          dirs.append(x)
       x='D:\\Program Files (x86)'
       if os.path.isdir(x) and x not in dirs:
          dirs.append(x)
    else:
       x='/usr'
       if os.path.isdir(x) and x not in dirs:
          dirs.append(x)
       x='/opt'
       if os.path.isdir(x) and x not in dirs:
          dirs.append(x)
       #
       # FIXME: Currently treating OSX as a subset of Linux:
       #
       if hosd.get('macos'):
          #
          # The location of software installed by brew prior to softlinking:
          #
          x='/usr/local/Cellar'
          if os.path.isdir(x) and x not in dirs:
             dirs.append(x)

    # Add from CK_TOOLS env
    x=os.environ.get(env_install_path,'')
    if x!='':
       dirs.append(x)

    # Add extra from CK_DIRS
    x=os.environ.get(env_search,'')
    if x!='':
       if hplat=='win':
          xx=x.split(';')
       else:
          xx=x.split(':')
       for x in xx:
           if x!='':
              dirs.append(x)

    # Check from input
    x=i.get('search_dirs','')
    if x!='':
       xx=x.split(',')

       for x in xx:
           if x!='':
              dirs.append(x)

    # Add user space
    from os.path import expanduser
    dirs.append(expanduser("~"))

    # Check if interactive
    iv='yes'
    quiet=i.get('quiet','')
    if quiet=='yes' or o!='con': iv=''

    # If there is a function to customize dirs, call it
    if 'dirs' in dir(cs):
       ii={"host_os_uoa":hosx,
           "host_os_uid":hos,
           "host_os_dict":hosd,
           "target_os_uoa":tosx,
           "target_os_uid":tos,
           "target_os_dict":tosd,
           "target_device_id":tdid,
           "cfg":d,
           "self_cfg":cfg,
           "ck_kernel":ck,
           "dirs":dirs,
           "interactive":iv
          }
       rx=cs.dirs(ii)
       if rx['return']>0: return rx
       if len(rx.get('dirs',[]))>0: dirs=rx['dirs']

    # Check which file to search for
    sname=i.get('soft_name','')
    if sname=='':
       ry=prepare_target_name({'host_os_dict':hosd,
                               'target_os_dict':tosd,
                               'cus':cus})
       if ry['return']>0: return ry
       sname=ry['tool']

    cbd=cus.get('soft_can_be_dir','')

    sen=cus.get('soft_extra_name','')

    osname=sname
    if sname=='':
       return {'return':1, 'error':'software description doesn\'t have a name of file to search ...'}

    # Check if search for extensions gcc-4.9, clang-3.8, etc
    if hplat=='linux' and cus.get('search_numeric_ext_on_linux','')=='yes':
       sname+='*'

    # Search tools
    suname=d.get('soft_name','')
    x=sname
    if suname!='': x=suname+' ('+sname+')'

    ck.out('')
    ck.out('  Searching for '+x+' to automatically register in the CK - it may take some time, please wait ...')
    ck.out('')

    rlm=cus.get('limit_recursion_dir_search',{}).get(hplat,0)

    skip_sort='no'

    fp=i.get('full_path','')
    if fp!='':
       lst=[fp]
    else:
       rx=search_tool({'path_list':dirs, 'file_name':sname, 'recursion_level_max':rlm, 'can_be_dir':cbd, 'out':'con'})
       if rx['return']>0: return rx

       lst=rx['list']
       et=rx['elapsed_time']

       # Limit to required ones
       if 'limit' in dir(cs):
          rx=cs.limit({'list':lst,
                       'host_os_dict':hosd,
                       'target_os_dict':tosd,
                       'soft_name':osname,
                       'ck_kernel':ck})
          if rx['return']>0: return rx
          lst=rx['list']
          if rx.get('skip_sort','')!='': skip_sort=rx['skip_sort']

    # Print results
#    if o=='con':
       ck.out('')
       ck.out('  Search completed in '+('%.1f' % et)+' secs. Found '+str(len(lst))+' target files (may be pruned) ...')

    # Select, if found
    il=0
    if len(lst)>0:
       # Trying to detect version
       if o=='con':
          ck.out('')
          ck.out('  Detecting and sorting versions (ignore some work output) ...')

       vlst=[]

       # Sometimes can be the same paths (due to soft links) - remove:
       lst1=[]
       lst2=[]
       for q in reversed(lst):
           q2=os.path.realpath(q)
           if q2 not in lst2:
              lst1.append(q)
              lst2.append(q2)
       lst=reversed(lst1) # return to original order if need to avoid sorting

       # Process each path
       if o=='con':
          ck.out('')

       for q in lst:
           kk={'path':q}

           pr=''
           if o=='con':
              pr='    * '+q

           # Try to detect version
           ver=''
           sver=[]
           ii={'full_path':q,
               'bat':sbat,
               'host_os_dict':hosd,
               'target_os_dict':tosd,
               'cmd':soft_version_cmd,
               'use_locale':cus.get('use_locale_for_version',''),
               'custom_script_obj':cs}
           rx=get_version(ii)
           if rx['return']>0:
              if o=='con':
                 pr+='\n        WARNING: '+rx['error']
           else:
              ver=rx['version']

              # Split version
              rx=split_version({'version':ver})
              if rx['return']>0: return rx
              sver=rx['version_split']

              kk['version']=ver
              kk['version_detected']=ver
              kk['version_split']=sver

              if o=='con':
                 pr+='   (Version '+ver+')'

           skip=False
           if len(vfrom)>0:
              r=compare_versions({'version1':vfrom, 'version2':sver})
              if r['return']>0: return r
              if r['result']=='>':  skip=True

           if not skip and len(vto)>0:
              r=compare_versions({'version1':sver, 'version2':vto})
              if r['return']>0: return r
              if r['result']=='>':  skip=True

           if skip: pr+=' - skipped because of version constraints!'

           if o=='con':
              ck.out(pr)

           if not skip and (cus.get('add_only_with_version','')!='yes' or ver!=''):
              vlst.append(kk)

       if o=='con':
          ck.out('')

       # Sort by version
       if skip_sort!='yes':
          vlst=sorted(vlst, key=lambda k: (internal_get_val(k.get('version_split',[]), 0, 0),
                                           internal_get_val(k.get('version_split',[]), 1, 0),
                                           internal_get_val(k.get('version_split',[]), 2, 0),
                                           internal_get_val(k.get('version_split',[]), 3, 0),
                                           internal_get_val(k.get('version_split',[]), 4, 0),
                                           k.get('path','')),
                     reverse=True)

       lst=[]
       for q in vlst:
           lst.append(q['path'])

       if len(lst)>1:
          if o=='con':
             ck.out('')

          if iv=='yes':
             ck.out('  Registering software installations found on your machine in the CK:')
             ck.out('')
             ck.out('    (HINT: enter -1 to force CK package installation)')
             ck.out('')

             iq=0

             for kk in vlst:
                 q=kk['path']
                 ver=kk.get('version','')

                 x=q
                 if ver!='':x='Version '+ver+' - '+x

                 ck.out('    '+str(iq)+') '+x)
                 iq+=1

             ck.out('')
             rx=ck.inp({'text':'    Please, select the number of any above installation or press Enter to select 0: '})
             xx=rx['string'].strip()
             if xx=='': xx='0'
             il=0
             try:
                il=int(xx)
             except:
                il=-1

             if il<0 or il>=len(lst):
                return {'return':1, 'error':'selection number is not recognized'}

    # If not found, quit
    if len(lst)==0:
       if i.get('skip_help','')!='yes':
          r=print_help({'data_uoa':duid, 'platform':hplat})
          # Ignore output

       return {'return':16, 'error':'software was not automatically found on your system! Please, install it and re-try again!'}

    # Check if CK install dict already exists
    pf=lst[il]

    env_data_uoa=i.get('force_env_data_uoa','')

    puoa=''

    dname=''
    xtags=''

    rx=find_config_file({'full_path':pf})
    if rx['return']>0: return rx
    found=rx['found']

    if found=='yes':
       dx=rx['dict']

       cus=dx.get('customize',{})

       ev=dx.get('extra_version','')

       if dx.get('env_data_uoa','')!='' and env_data_uoa=='':
          env_data_uoa=dx['env_data_uoa']

       dname=d.get('soft_name','')
       if cus.get('package_extra_name','')!='':
          dname+=cus['package_extra_name']

       puoa=dx.get('package_uoa','')

       xtags=dx.get('tags','')

       # FGG: should I add deps here or not - the thing is that the env 
       # most likely changed so probably not ...

       # New update -> I can now restore UIDs with deps, so maybe it's ok ...

       if o=='con':
          ck.out('')
          ck.out('  Found pre-recorded CK installation info ...')

    # Check if extra tags
    etags=i.get('extra_tags','').strip()
    if len(etags)>0:
       y=xtags.split(',')
       x=etags.split(',')

       for z in x:
           if z not in y:
              y.append(z)

       xtags=','.join(y)

    en=i.get('extra_name','')
    if en!='':
       en=' '+en

    # Attempt to register in CK
    if o=='con':
       ck.out('')
       ck.out('  Registering in the CK ('+pf+') ...')
       ck.out('')

    ii={'data_uoa':duid,
        'customize':cus,
        'full_path':pf,
        'quiet':quiet,
        'host_os':hos,
        'target_os':tos,
        'target_device_id':tdid,
        'deps':deps,
        'env':envx,
        'env_data_uoa':env_data_uoa,
        'soft_name':dname,
        'soft_add_name':en,
        'package_uoa':puoa,
        'extra_version':ev,
        'tags':xtags,
        'out':oo}

    if cus.get('collect_device_info','')!='yes':
        ii['skip_device_info_collection']='yes'

    rz=setup(ii)
    if rz['return']>0: return rz

    xeduoa=rz['env_data_uoa']
    xeduid=rz['env_data_uid']

    if o=='con':
       ck.out('  Successfully registered with UID: '+xeduid)

    return rz

##############################################################################
# get version of a given software (internal)

def get_version(i):
    """
    Input:  {
              full_path
              bat
              cmd

              custom_script_obj
              host_os_dict

              (show)                 - if 'yes', show output file

              (skip_existing)        - if 'yes', force detecting version again
              (skip_add_target_file) - if 'yes', do not add target file at the beginning 
                                       of CMD to detect version

              (use_locale)           - if 'yes', use locale to decode output
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              version      - string version
              version_lst  - raw output (as list)
            }

    """

    import os

    o=i.get('out','')

    fp=i.get('full_path','')
    sb=i.get('bat','')
    soft_version_cmd=i.get('cmd','')

    cs=i.get('custom_script_obj','')
    if cs=='': cs=None

    hosd=i.get('host_os_dict',{})
    tosd=i.get('target_os_dict',{})

    bprefix=hosd.get('batch_prefix','')
    ubtr=hosd.get('use_bash_to_run','')
    svarb=hosd.get('env_var_start','')
    svarb1=hosd.get('env_var_extra1','')
    svare=hosd.get('env_var_stop','')
    svare1=hosd.get('env_var_extra2','')
    sexe=hosd.get('set_executable','')
    sbp=hosd.get('bin_prefix','')
    envsep=hosd.get('env_separator','')
    scall=hosd.get('env_call','')
    sext=hosd.get('script_ext','')
    eifsc=hosd.get('env_quotes_if_space_in_call','')
    nout=hosd.get('no_output','')

    sb=bprefix+sb

    ver=''
    lst=[]

    # Attempt to check via CK config file
    if i.get('skip_existing','')!='yes':
       rx=find_config_file({'full_path':fp})
       if rx['return']>0: return rx
       found=rx['found']
       if found=='yes':
          ver=rx['dict'].get('customize',{}).get('version','')

    if ver=='':
       # Generate tmp file
       rx=ck.gen_tmp_file({})
       if rx['return']>0: return rx
       ftmp=rx['file_name']

       # Preparing CMD
       if 'version_cmd' in dir(cs):
          rx=cs.version_cmd({'full_path':fp,
                             'host_os_dict':hosd,
                             'target_os_dict':tosd,
                             'cmd':soft_version_cmd,
                             'ck_kernel':ck,
                             'out':o})
          if rx['return']>0: return rx
          cmd=rx.get('cmd','')
          ver=rx.get('version','')
       else:    
          if eifsc!='' and fp.find(' ')>=0 and not fp.startswith(eifsc):
             fp=eifsc+fp+eifsc

          cmd=''

          if o!='con':
             cmd+=nout

          if i.get('skip_add_target_file','')=='yes':
             cmd+=' '+soft_version_cmd
          else:
             cmd+=fp+' '+soft_version_cmd

    if ver=='':
       if 'parse_version' not in dir(cs):
          return {'return':22, 'error':'do not know how to detect version of a given software'}
 
       cmd=cmd.replace('$#filename#$', ftmp)

       if o=='con':
          ck.out('')
          ck.out('  Prepared CMD to detect version: '+cmd+' ...')

       # Finalizing batch file
       sb+='\n'+cmd+'\n'

       # Record to tmp batch and run
       rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':sext, 'remove_dir':'no'})
       if rx['return']>0: return rx
       fnb=rx['file_name']

       rx=ck.save_text_file({'text_file':fnb, 'string':sb})
       if rx['return']>0: return rx

       # Executing script
       y=''
       if sexe!='':
          y+=sexe+' '+fnb+envsep
       y+=' '+scall+' '+fnb

       if ubtr!='': y=ubtr.replace('$#cmd#$',y)

       if o=='con':
          ck.out('')
          ck.out('Executing "'+y+'" ...')

       ry=os.system(nout+y)
       # ignore return code (checking output file instead)

       os.remove(fnb)

       if os.path.isfile(ftmp): 
          import sys
          import locale

          en=sys.stdout.encoding
          if i.get('use_locale','')=='yes':
             en=locale.getdefaultlocale()[1]

          rx=ck.load_text_file({'text_file':ftmp, 'split_to_list':'yes', 'encoding':en})
          if rx['return']>0: return rx
          lst=rx['lst']

          os.remove(ftmp)

       if len(lst)==0:
          return {'return':16, 'error':'version output file is empty'}

       if i.get('show','')=='yes':
          ck.out('Output:')
          ck.out('')
          for q in lst:
              ck.out('  '+q)

       # Calling customized script to parse version
       ii={'output':lst,
           'host_os_dict':hosd,
           'ck_kernel':ck}
       rx=cs.parse_version(ii)
       if rx['return']>0 and rx['return']!=16: return rx

       ver=rx.get('version','')

    if ver=='':
       return {'return':16, 'error':'version was not detected'}

    if o=='con':
       ck.out('')
       ck.out('Version detected: '+ver)

    return {'return':0, 'version':ver, 'version_lst':lst} 

##############################################################################
# internal function: get value from list without error if out of bounds

def internal_get_val(lst, index, default_value):
    v=default_value
    if index<len(lst):
       v=lst[index]
    return v

##############################################################################
# print help for this software entry

def print_help(i):
    """
    Input:  {
              data_uoa - data UOA to get help
              platform - platform name 
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    duoa=i['data_uoa']
    hplat=i['platform']

    ti=''
    # If only one related software entry found, try to read text notes from it 
    rx=ck.access({'action':'find',
                  'module_uoa':work['self_module_uid'],
                  'data_uoa':duoa})
    if rx['return']>0: return rx
    pppx=rx['path']

    ppx=os.path.join(pppx,'install.txt')
    if os.path.isfile(ppx):
       rx=ck.load_text_file({'text_file':ppx})
       if rx['return']==0:
          ti+=rx['string']

    ppx=os.path.join(pppx,'install.'+hplat+'.txt')
    if os.path.isfile(ppx):
       rx=ck.load_text_file({'text_file':ppx})
       if rx['return']==0:
          if ti!='': ti+='\n'
          ti+=rx['string']

    if ti!='':
       read=True

       ck.out('****** Installation notes: ******')

       ck.out(ti)

       ck.out('*********************************')

    else:
       # Show possible Wiki page
       rx=ck.inp({'text':'       Would you like to open wiki pages about installation and other info (if exists) (Y/n): '})
       x=rx['string'].strip().lower()

       if x!='n' and x!='no':
          ck.out('')
          rx=ck.access({'action':'wiki',
                        'module_uoa':work['self_module_uid'],
                        'data_uoa':duoa})
          if rx['return']>0: return rx
          ck.out('')

    return {'return':0}

##############################################################################
# check that host and target OS is supported

def check_target(i):
    """
    Input:  {
              dict           - dictionary with info about supported host and target OS

              host_os_uoa    - host OS UOA  (already resolved)
              host_os_dict   - host OS dict (already resolved)

              target_os_uoa  - target OS UOA  (already resolved)
              target_os_dict - target OS UOA  (already resolved)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    cus=i['dict']

    hosx=i['host_os_uoa']
    hosd=i['host_os_dict']

    tosx=i['target_os_uoa']
    tosd=i['target_os_dict']

    # Check if restricts dependency to a given host or target OS
    only_hos=cus.get('only_for_host_os',[])
    if len(only_hos)>0:
       if hosx not in only_hos:
          return {'return':1, 'error':'host OS is not supported by this software'}

    only_hos1=cus.get('only_for_host_os_tags',[])
    if len(only_hos1)>0:
       x=hosd.get('tags',[])
       found=False
       for xx in only_hos1:
           if xx in x:
              found=True
              break
       if not found:
          return {'return':1, 'error':'host OS family is not supported by this software'}

    only_tos=cus.get('only_for_target_os',[])
    if len(only_tos)>0:
       if tosx not in only_tos:
          return {'return':1, 'error':'target OS is not supported by this software'}

    only_tos1=cus.get('only_for_target_os_tags',[])
    if len(only_tos1)>0:
       x=tosd.get('tags',[])
       found=False
       for xx in only_tos1:
           if xx in x:
              found=True
              break
       if not found:
          return {'return':1, 'error':'target OS family is not supported by this software'}

    return {'return':0}

##############################################################################
# split version

def split_version(i):
    """
    Input:  {
              version - string version
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              version_split - split version
            }

    """

    import re

    ver=i['version']

    # Split version
    sver=[]
    if ver!='':
       if ver!='':
          sver1=re.split('\.|\-|\_', ver)
          for q in sver1:
              x=q
              try:
                 x=int(q)
              except:
                 #pass - causes problems when mixing strings and ints ...
                 x=0
              sver.append(x)

    return {'return':0, 'version_split':sver}

##############################################################################
# show available software descriptions

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
       h+='<i><b>Note:</b> you can detect softare and register it in the CK via <pre>$ ck detect soft:{soft UOA} (--target_os=android21-arm64)</i><br><br>\n'
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

           ad=lm.get('auto_detect','')
           if ad!='yes': ad='no'

           ep=cus.get('env_prefix','')

           xhos=cus.get('only_for_host_os_tags',[])
           xtos=cus.get('only_for_target_os_tags',[])

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
                 y='['+url+'/tree/master/soft/'+ln+' link]'
              ck.out('')
              ck.out('=== '+ln+' ('+name+') ===')
              ck.out('')
              ck.out('Auto-detect?: '+ad)
              ck.out('<br>Environment variable: <b>'+ep+'</b>')
              ck.out('')
              ck.out('Tags: <i>'+ytags+'</i>')
              ck.out('<br>Host OS tags: <i>'+yhos+'</i>')
              ck.out('<br>Target OS tags: <i>'+ytos+'</i>')
              if y!='':
                 ck.out('')
                 ck.out('Software entry with meta: <i>'+y+'</i>')
              ck.out('')
              ck.out('Which CK repo: '+x)
              if to_get!='':
                 ck.out('<br>How to get: <i>'+to_get+'</i>')
              if to_get!='':
                 ck.out('')
                 ck.out('How to detect: <b>ck detect soft:'+ln+' (--target_os={CK OS UOA})</b>')
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
# get version of a given software (internal)

def find_config_file(i):
    """
    Input:  {
              full_path  - where to start search
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              found    - 'yes' if found
              dict     - loaded dict with the configuration ...
              filename - filename
              path     - path
            }

    """

    import os

    pf=i['full_path']

    pf1=os.path.dirname(pf)

    found='no'
    d={}

    fn=''
    pf2=''
    while pf1!=pf and pf1!='':
       fn=cfg['ck_install_file']
       pf2=os.path.join(pf1,fn)
       if os.path.isfile(pf2):
          rx=ck.load_json_file({'json_file':pf2})
          if rx['return']==0:
             found='yes'
             d=rx['dict']
             break
       else:
          fn=cfg['ck_install_file_saved']
          pf2=os.path.join(pf1,fn)
          if os.path.isfile(pf2):
             rx=ck.load_json_file({'json_file':pf2})
             if rx['return']==0:
                found='yes'
                d=rx['dict']
                break

       pf=pf1
       pf1=os.path.dirname(pf)

    return {'return':0, 'found':found, 'dict':d, 'filename':fn, 'path':pf2}

##############################################################################
# compare two versions (in list)

def compare_versions(i):
    """
    Input:  {
              version1 - version 1 to compare against version2 (list such as [1,62])
              version2 - (list such as [1,63])
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              result       "<" - version 1 < version 2
                           "=" - version 1 == version 2
                           ">" - version 1 > version 2
            }

    """

    def compare_versions_core(v1_orig, v2_orig):

        len_diff = len(v2_orig)-len(v1_orig)    # determine the (signed) length of zero-padding

        # now pad the shorter to match the longer:
        (v1, v2) = (v1_orig + [0]*len_diff, v2_orig) if len_diff>0 else (v1_orig, v2_orig + [0]*-len_diff)

        for j in range(0,len(v1)):
            (t1, t2) = (type(v1[j]), type(v2[j]))
            if t1 == t2:        # perform natural comparison within the same type
                if v1[j]<v2[j]:
                    return '<'
                elif v1[j]>v2[j]:
                    return '>'
            elif t1 == int:     # but any integer is higher than any letter combination
                return '>'
            elif t2 == int:
                return '<'

        return '='

    result = compare_versions_core(i['version1'], i['version2'])

    if i.get('out','')=='con':
       ck.out(result)

    return {'return':0, 'result':result}

##############################################################################
# compare two versions (in list)

def prepare_target_name(i):
    """
    Input:  {
              host_os_dict   - host OS dict
              target_os_dict - target OS dict
              cus            - custom meta
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              tool         - tool name
            }

    """

    cus=i['cus']

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    hplat=hosd['ck_name']
    tplat=tosd['ck_name']

    tool=''

    plat=tplat
    osd=tosd
    if cus.get('soft_file_from_host_os','')=='yes':
       plat=hplat
       osd=hosd

    tool=cus.get('soft_file_universal','')
    if tool=='':
       tool=cus.get('soft_file',{}).get(plat,'')

    file_extensions=hosd.get('file_extensions',{})

    # Check file extensions from OS (for example, to specialize .dylib vs .so for MacOS)
    for k in file_extensions:
        v=file_extensions[k]

        tool=tool.replace('$#file_ext_'+k+'#$',v)

    return {'return':0, 'tool':tool}
