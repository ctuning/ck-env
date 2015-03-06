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

              (tool)              - force this tool name
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
    tool=i.get('tool','')
    if tool=='':
       tool=d.get('tool','')

    cmd=tool+' '+ver.get('cmd','')
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
    else:
       if o=='con':
          ck.out('Version detected: V'+dver)

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

              (data_name)         - use this user friendly name for environment entry

              (customize)         - dict with custom parameters 
                                    (usually passed to customize script)

                                    skip_add_dirs
                                    skip_add_to_path
                                    skip_add_to_ld_path

                                    version      - add this version
                                    skip_version - if 'yes', do not add version

              (env)               - update default env with this dict

              (deps)              - list with dependencies (in special format, possibly resolved (from package))

              (install_path)      - path with soft is installed

              (bat_file)          - if !='', record environment to this bat file, 
                                    instead of creating env entry

              (quiet)             - if 'yes', minimize questions
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
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
                 'os':hos,
                 'skip_info_collection':'yes'})
    if r['return']>0: return r
    hos=r['os_uid']
    hosx=r['os_uoa']
    hosd=r['os_dict']

    # Checking/detecting host OS
    r=ck.access({'action':'detect',
                 'module_uoa':cfg['module_deps']['platform.os'],
                 'os':tos,
                 'device_id':tdid,
                 'skip_info_collection':'yes'})
    if r['return']>0: return r
    tos=r['os_uid']
    tosx=r['os_uoa']
    tosd=r['os_dict']
    tdid=r['device_id']

    # Check environment UOA
    duoa=i.get('uoa','')
    duid=''
    dname=i.get('data_name','')

    tags=i.get('tags','')

    if duoa=='': duoa=i.get('data_uoa','')

    if duoa=='':
       xcids=i.get('xcids',[])
       if len(xcids)>0:
          duoa=xcids[0].get('data_uoa','')

    if duoa=='':
       # Search
       if tags!='':
          r=ck.access({'action':'search',
                       'module_uoa':work['self_module_uid'],
                       'tags':tags})
          if r['return']>0: return r
          l=r['lst']
          if len(l)>0:
             duid=l[0].get('data_uid')
             duoa=duid
             if dname=='': 
                dname=l[0].get('data_name','')

    d={}
    p=''

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
    else:
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

    ltags=d.get('tags',[])

    # Check deps
    deps=d.get('deps',[])
    udeps=i.get('deps',[])
    if len(udeps)>0: deps=udeps

    # Add tags from the search!
    for q in tags.split(','):
        q1=q.strip()
        if q1 not in ltags: ltags.append(q1)

    if o=='con':
       if duoa!='' and duid!='':
          x=duoa
          if duid!=duoa: x+=' ('+duid+')'
       else:
          x='local directory'
       ck.out('Software entry found: '+x)

    # Get customize dict
    cus=i.get('customize',{})

    # Check installation path
    pi=i.get('install_path','')
    if pi=='':
       if o=='con':
          ck.out('')
          r=ck.inp({'text':'Enter path to installed tool: '})
          pi=r['string']

       if pi=='':
          return {'return':1, 'error':'installation path is not specified'}

    # Check version
    ver=cus.get('version','')
    if ver=='' and o=='con' and cus.get('skip_version','')!='yes':
       ck.out('')
       r=ck.inp({'text':'Enter tool version (or Enter to skip): '})
       ver=r['string']

    ver_int=cus.get('version_int','')
    if ver=='' and o=='con' and cus.get('skip_version','')!='yes':
       ck.out('')
       r=ck.inp({'text':'Enter integer tool version for comparison (for V5.2.3 use 50203): '})
       verx=r['string']
       if verx=='': verx='0'
       ver_int=int(verx)

    # Prepare environment and batch
    sb=''

    ep=d.get('env_prefix','')
    sdirs=hosd.get('dir_sep','')

    wb=tosd.get('windows_base','')

    tbits=tosd.get('bits','')

    envp=d.get('env_prefix','')

    rem=hosd.get('rem','')
    eset=hosd.get('env_set','')
    svarb=hosd.get('env_var_start','')
    svare=hosd.get('env_var_stop','')
    sdirs=hosd.get('dir_sep','')
    evs=hosd.get('env_var_separator','')
    eifs=hosd.get('env_quotes_if_space','')

    misc={'env_prefix':ep}

    # If install path has space, add quotes for some OS ...
    xs=''
    if pi.find(' ')>=0 and eifs!='':
       xs=eifs

    tg='host-os-'+hosx
    if tg not in ltags: ltags.append(tg)

    tg='target-os-'+tosx
    if tg not in ltags: ltags.append(tg)

    tg=tbits+'bits'
    if tg not in ltags: ltags.append(tg)

    lenv=d.get('lenv',[])
    env={}

    for q in lenv:
        k=q[0]
        v=q[1]

        k=k.replace('$#env_prefix#$', ep)
        v=v.replace('$#install_path#$', pi)
        v=v.replace('$#dir_sep#$',sdirs)

        env[k]=v

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
       ii={"host_os_uoa":hos,
           "target_os_uoa":tos,
           "target_bits":tbits,
           "host_os_dict":hosd,
           "target_os_dict":tosd,
           "target_device_id":tdid,
           "host_os_uid":hos,
           "host_os_uoa":hosx,
           "target_os_uid":tos,
           "target_os_uoa":tosx,
           "target_os_bits":tbits,
           "soft_uoa":duoa,
           "tags":ltags,
           "cfg":d,
           "env":env,
           "deps":deps,
           "path":pi,
           "customize":cus
          }

       if o=='con': ii['interactive']='yes'
       if i.get('quiet','')=='yes' and cus.get('interactive','')!='yes':
          ii['interactive']=''

       rx=crx.setup(ii)
       if rx['return']>0: return rx
       env=rx['env']
       deps=rx.get('deps',[])
       ltags=rx['tags']
       sadd=rx['bat']

    # If user env, update it
    xenv=i.get('env',{})
    if len(xenv)>0:
       env.update(xenv)

    # Resolve deps
    sdeps=''
    res=[]
    if len(deps)>0:
       rx=ck.access({'action':'resolve',
                     'module_uoa':cfg['module_deps']['env'],
                     'host_os':hos,
                     'target_os':tos,
                     'target_device_id':tdid,
                     'deps':deps})
       if rx['return']>0: return rx
       sdeps=rx['bat']
       deps=rx['deps'] # Update deps (add UOA)
       res=rx['res_deps']

    # Finish batch
    # Echo Off
    sb+=hosd.get('batch_prefix','')+'\n'

    x=duoa
    if len(tags)>0:
       y=''
       for q in ltags:
           if y!='': y+=','
           y+=q
       x+=' ('+y+')'
    sb+=rem+' '+'Soft UOA         = '+x+'\n'

    sb+=rem+' '+'Host OS UOA      = '+hosx+'\n'
    sb+=rem+' '+'Target OS UOA    = '+tosx+'\n'
    sb+=rem+' '+'Target OS bits   = '+tbits+'\n'
    if ver!='':
       sb+=rem+' '+'Tool version     = '+ver+'\n'
       misc['version']=ver
    if ver_int!=0:
       sb+=rem+' '+'Tool int version = '+str(ver_int)+'\n'
       misc['version_int']=ver_int
    sb+='\n'

    if sdeps!='':
       sb+=rem+' Dependencies\n'
       sb+=sdeps+'\n'

    if sadd!='':
       sb+=sadd

    if cus.get('skip_add_dirs','')!='yes':
       envp_i=envp
       sb+=eset+' '+envp_i+'='+xs+pi+xs+'\n'
       misc['path_install']=pi

       envp_b=envp+'_BIN'
       pib=pi+sdirs+'bin'
       sb+=eset+' '+envp_b+'='+xs+pib+xs+'\n'
       misc['path_bin']=pib

       if cus.get('skip_add_to_ld_lib','')!='yes':
          envp_l=envp+'_LIB'
          plib=pi+sdirs+'lib64'
          if tbits=='64' and not os.path.isdir(plib):
             plib=pi+sdirs+'lib32'
             if not os.path.isdir(plib):
                plib=pi+sdirs+'lib' 
#                if not os.path.isdir(plib):
#                   return {'return':1, 'error':'can\'t find lib path'}
          sb+=eset+' '+envp_l+'='+xs+plib+xs+'\n\n'
          misc['path_lib']=plib

    # Add all env
    for k in sorted(env):
        v=env[k]
        sb+=eset+' '+k+'='+v+'\n'
    sb+='\n'

    # Add to existing vars
    if cus.get('skip_add_to_path','')!='yes':
       sb+=eset+' PATH='+svarb+envp_b+svare+evs+svarb+'PATH'+svare+'\n'

    if cus.get('skip_add_to_ld_path','')!='yes':
       sb+=eset+' LD_LIBRARY_PATH='+svarb+envp_l+svare+evs+svarb+'LD_LIBRARY_PATH'+svare+'\n\n'

    # Finish batch
    if wb=='yes':
       sb+='exit /b 0\n'

    # Check meta
    setup={'host_os_uoa':hos,
           'target_os_uoa':tos,
           'target_os_bits':tbits}
    if ver!='': 
       setup['version']=ver
       tg='v'+ver
       if tg not in ltags: ltags.append(tg)

    search_dict={'setup':setup}

    # Finish tags
    stags=''
    for q in ltags:
        if stags!='': stags+=','
        stags+=q.strip()

    # Check if save to bat file
    bf=i.get('bat_file', '')
    pnew=''
    finish=False

    if bf=='':
       bf=cfg['default_bat_name']+hosd.get('script_ext','')

       if o=='con':
          ck.out('')
          ck.out('Searching if environment already exists using tags:')
          ck.out('  '+stags)

       r=ck.access({'action':'search',
                    'module_uoa':cfg['module_deps']['env'],
                    'tags':stags,
                    'search_dict':search_dict})
       if r['return']>0: return r
       lst=r['lst']

       # Preparing to add or update entry
       xx='added'

       dd={'tags':ltags,
           'setup':setup,
           'env':env,
           'deps':deps,
           'resolved_deps_uoa':res,
           'misc':misc,
           'env_script':bf}

       ii={'action':'add',
           'module_uoa':cfg['module_deps']['env'],
           'dict':dd,
           'sort_keys':'yes',
           'substitute':'yes'}

       if len(lst)>0:
          fe=lst[0]

          eduoa=fe['data_uoa']
          eduid=fe['data_uid']

          if o=='con':
             x=eduoa
             if eduid!=eduoa: x+=' ('+eduid+')'

             ck.out('')
             ck.out('Environment found: '+x)

             if i.get('update','')!='yes':
                if o=='con':
                   ck.out('')
                   r=ck.inp({'text':'Would you like to update this entry (Y/n): '})
                   upd=r['string'].strip().lower()

                   if upd!='' and upd!='y' and upd!='yes':
                      finish=True

             if not finish:
                ii['action']='update'
                ii['data_uoa']=eduid
                xx='updated'

       # Adding/updating
       if not finish:
          if dname!='':
             ii['data_name']=dname

          rx=ck.access(ii)
          if rx['return']>0: return rx

          eduoa=rx['data_uoa']
          eduid=rx['data_uid']

          pnew=rx['path']

          if o=='con':
             ck.out('')
             ck.out('Environment entry '+xx+' ('+eduoa+')!')

    # Record batch file
    if not finish:
       if pnew=='': pb=bf
       else:        pb=os.path.join(pnew, bf)

       # Write file
       rx=ck.save_text_file({'text_file':pb, 'string':sb})
       if rx['return']>0: return rx

    return {'return':0}
