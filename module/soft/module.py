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

    # Check if has version
    ver=d.get('version','')

    tool=ver.get('tool_via_env','')
    if tool!='':
       tool=svarb+svarb1+tool+svare1+svare
    else:
       tool=d.get('tool','')

    if i.get('tool','')!='':
       tool=i['tool']

    cmd=tool+' '+ver.get('cmd','')
    lst=[]

    dver=''
    lver=[]

    if cmd!='':
       rx=ck.gen_tmp_file({})
       if rx['return']>0: return rx
       fn=rx['file_name']

       cmd=cmd.replace('$#filename#$', fn)

       if env!='': cmd=env.strip()+'\n'+cmd

       # Record to tmp batch and run
       rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':sext, 'remove_dir':'yes'})
       if rx['return']>0: return rx
       fnb=rx['file_name']

       rx=ck.save_text_file({'text_file':fnb, 'string':cmd})
       if rx['return']>0: return rx

       y=''
       if sexe!='':
          y+=sexe+' '+sbp+fnb+envsep
       y+=' '+scall+' '+sbp+fnb

       if ubtr!='': y=ubtr.replace('$#cmd#$',y)

       if o=='con':
          ck.out('')
          ck.out('Executing cmd: '+y+' ...')

       ry=os.system(y)
#       if ry>0:
#          return {'return':16, 'error':'executing command returned non-zero value ('+cmd+')'}

       if os.path.isfile(fn): 
          import sys
          rx=ck.load_text_file({'text_file':fn, 'split_to_list':'yes', 'encoding':sys.stdout.encoding})
          if rx['return']>0: return rx
          lst=rx['lst']

          os.remove(fn)

    if len(lst)==0:
       return {'return':16, 'error':'version output file is empty'}

    if i.get('show','')=='yes':
       ck.out('Output:')
       ck.out('')
       for q in lst:
           ck.out('  '+q)

    dver=''
    cl=ver.get('check_lines',-1)

    jj=0
    for s in lst:
        jj+=1
        if cl!=-1 and jj>cl: break

        sbefore=ver.get('string_before','')
        safter=ver.get('string_after','')
        safter1=ver.get('string_after1','')
        safter_rel=ver.get('string_after_relaxed','')

        i1=0
        i2=len(s)

        if sbefore!='':
           i1=s.find(sbefore)
           if i1<0: continue

        if safter!='':
           if sbefore!='': i2=s.find(safter, i1+len(sbefore)+1)
           else: i2=s.find(safter)

           if i2<0 and safter1!='':
              if safter1=='@@@': i2=len(s)
              else:
                if sbefore!='': i2=s.find(safter1, i1+len(sbefore)+1)
                else: i2=s.find(safter1)

           if i2<0: continue
        elif safter_rel!='':
           if sbefore!='': i3=s.find(safter_rel, i1+len(sbefore)+1)
           else: i3=s.find(safter_rel)

           if i3>=0: i2=i3

        dver=s[i1+len(sbefore):i2].strip()

        spl=ver.get('split','')
        if spl!='':
           lver=dver.split(spl)

        break

    if dver=='':
       return {'return':16, 'error':'version was not detected'}
    else:
       if o=='con':
          ck.out('Version detected: '+dver)

    return {'return':0, 'version_str':dver, 
                        'version_lst':lver, 
                        'version_raw':lst}

##############################################################################
# setup environment

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

              (bat_file)          - if !='', record environment to this bat file, 
                                    instead of creating env entry

              (quiet)             - if 'yes', minimize questions

              (env_data_uoa)      - use this data UOA to record (new) env
              (env_repo_uoa)      - use this repo to record new env
              (env_new)           - if 'yes', do not search for environment (was already done in package, for example)

              (package_uoa)       - if called from package, record package_uoa just in case

              (reset_env)         - if 'yes', do not use environment from existing entry, but use original one
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              env_data_uoa - environment entry UOA
              env_data_uid - environment entry UID
            }

    """

    import os

    o=i.get('out','')

    ########################################################################
    # Check host/target OS/CPU
    hos=i.get('host_os','')

    tos=i.get('target_os','')
    if tos=='':
       tos=cfg.get('default_target_os_uoa','')

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

    tbits=tosd.get('bits','')

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

    dname=d.get('soft_name','')
    if i.get('soft_name','')!='': dname=i['soft_name']

    if o=='con':
       if duoa!='' and duid!='':
          x=': '+duoa
          if duid!=duoa: x+=' ('+duid+')'
       else:
          x=' in local directory'
       ck.out('Software entry found'+x)

    # Check deps, customize, install path
    ltags=d.get('tags',[])
    deps=d.get('deps',{})
    env=d.get('env',{})
    cus=d.get('customize',{})
    pi=''
    envp=cus.get('env_prefix','')
    envps=envp+'_SET'

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
          if i.get('reset_env','')!='yes':
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
        setup['deps_'+q]=v['uoa']

    ########################################################################
    # Check version
    ver=cus.get('version','')
    if ver==''  and cus.get('skip_version','')!='yes' and o=='con':
       ck.out('')
       r=ck.inp({'text':'Enter soft version: '})
       ver=r['string']

    if ver!='': 
       setup['version']=ver
       tg='v'+ver
       if tg!='' and tg not in ltags: ltags.append(tg)

       # Separate version into subversions for tags
       if tg!='':
          ltags1=[]
          mf=tg.rfind('.')
          if tg.startswith('v') and mf>=0:
             while mf>=0:
                   t=tg[:mf]
                   if t not in ltags:
                      ltags1.append(t)
                   mf=tg.rfind('.',0,mf-1)

          if len(ltags1)>0:
             for z in ltags1:
                 ltags.append(z)

    # Finish tags
    stags=''
    for q in ltags:
        if q!='':
           if stags!='': stags+=','
           stags+=q.strip()

    ########################################################################
    # Search
    finish=False
    if enduoa=='' and i.get('env_new','')!='yes':
       if o=='con':
          ck.out('')
          ck.out('Searching if environment already exists using:')
          ck.out('  * Tags: '+stags)
          if len(deps)>0:
             for q in deps:
                 v=deps[q]
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
             ck.out('Environment found: '+x)

             if i.get('update','')!='yes':
                if o=='con':
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
             ck.out('Environment not found ...')

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
       if cus.get('skip_path','')!='yes' and i.get('skip_path','')!='yes':
          if o=='con':
             if update:
                ck.out('')
                ck.out('Current path to installed tool: '+pi)
                r=ck.inp({'text':'Input new path to installed tool or press Enter to keep old: '})
                pix=r['string'].strip()
                if pix!='': pi=pix
             elif pi=='':
                ck.out('')
                ye=cus.get('input_path_example','')
                if ye!='': y=' (example: '+ye+')'
                else: y=''
                r=ck.inp({'text':'Enter path to installed tool'+y+': '})
                pi=r['string'].strip()

          if pi=='':
             return {'return':1, 'error':'installation path is not specified'}

       ver_int=cus.get('version_int',0)
       if ver_int==0 and o=='con' and cus.get('skip_version','')!='yes':
          ck.out('')
          r=ck.inp({'text':'Enter soft version as integer for comparison (for V5.2.3 use 50203): '})
          verx=r['string'].strip()
          if verx=='': verx='0'
          ver_int=int(verx)

       if pi!='':
          cus['path_install']=pi

       if cus.get('skip_add_dirs','')!='yes' and pi!='':
          if cus.get('add_include_path','')=='yes':
             pii=pi+sdirs+'include'
             cus['path_include']=pii

          if cus.get('skip_add_to_bin','')!='yes':
             pib=pi
             if cus.get('skip_add_bin_ext','')!='yes': pib+=sdirs+'bin'
             cus['path_bin']=pib

          if cus.get('skip_add_to_ld_path','')!='yes':
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

       # If install path has space, add quotes for some OS ...
       xs=''
       if pi.find(' ')>=0 and eifs!='':
          xs=eifs

       # Check if customization script
       customize_script=d.get('customize_script','')
       sadd=''
       if customize_script!='':
          # Check individual prepare script
          rx=ck.load_module_from_path({'path':p, 'module_code_name':customize_script, 'skip_init':'yes'})
          if rx['return']>0: return rx
          crx=rx['code']

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
              "customize":cus
             }

          if o=='con': ii['interactive']='yes'
          if i.get('quiet','')=='yes': ii['interactive']=''

          rx=crx.setup(ii)
          if rx['return']>0: return rx

          sadd=rx['bat']
          pi=cus.get('path_install','')

          if cus.get('soft_name','')!='':
             dname=cus['soft_name']

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
       sb+=rem+' '+'Soft UOA         = '+x+'\n'

       sb+=rem+' '+'Host OS UOA      = '+hosx+' ('+hos+')\n'
       sb+=rem+' '+'Target OS UOA    = '+tosx+' ('+tos+')\n'
       sb+=rem+' '+'Target OS bits   = '+tbits+'\n'
       if ver!='':
          sb+=rem+' '+'Tool version     = '+ver+'\n'
          cus['version']=ver
       if ver_int!=0:
          sb+=rem+' '+'Tool int version = '+str(ver_int)+'\n'
          cus['version_int']=ver_int
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

       if cus.get('skip_add_dirs','')!='yes' and pi!='':
          if pib!='' and cus.get('skip_add_to_bin','')!='yes': sb+=eset+' '+envp_b+'='+xs+pib+xs+'\n'
          if plib!='': sb+=eset+' '+envp_l+'='+xs+plib+xs+'\n'
          if piib!='': sb+=eset+' '+envp_i+'='+xs+piib+xs+'\n'

       if sadd!='':
          sb+='\n'+sadd

       # Add all env
       for k in sorted(env):
           v=env[k]

           if eifs!='' and wb!='yes':
              if v.find(' ')>=0 and not v.startswith(eifs):
                 v=eifs+v+eifs

           sb+=eset+' '+k+'='+v+'\n'
       sb+='\n'

       # Add to existing vars
       if cus.get('skip_add_to_path','')!='yes' and cus.get('skip_add_to_bin','')!='yes' and cus.get('skip_dirs','')!='yes' and pi!='':
          sb+=eset+' PATH='+svarb+envp_b+svare+evs+svarb+'PATH'+svare+'\n'

       if cus.get('skip_add_to_ld_path','')!='yes' and cus.get('skip_dirs','')!='yes' and pi!='':
          sb+=eset+' '+elp+'='+svarb+envp_l+svare+evs+svarb+elp+svare+'\n'
          sb+=eset+' '+ellp+'='+svarb+envp_l+svare+evs+svarb+ellp+svare+'\n'

       # Say that environment is set (to avoid recursion)
       sb+=eset+' '+envps+'=1\n'

       # Finish batch
       if wb=='yes':
          sb+='\n'
          sb+='exit /b 0\n'

       # Check if save to bat file
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

    return {'return':0, 'env_data_uoa':enduoa, 'env_data_uid':enduid}
