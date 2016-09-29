#
# Collective Knowledge (description of a given machine for crowd-benchmarking and crowd-tuning)
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
line='***************************************************************************************'

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
# add new machine description

def add(i):
    """
    Input:  {
              (data_uoa) or (alias)        - force name of CK entry to store description of this machine
                                             (if empty, suggest automatically)

              (host_os)                    - host OS (detect, if omitted)
              (target_os)                  - OS module to check (if omitted, analyze host)
              (device_id)                  - device id if remote (such as adb)

              (use_host)                   - if 'yes', configure host as target

              (access_type)                - access type to the machine ("android", "mingw", "wa_android", "wa_linux", "ck_node", "ssh")

              (share)                      - if 'yes', share public info about platform with the community via cknowledge.org/repo
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import copy
    import os

    # Setting output
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    # Params
    hos=i.get('host_os','')
    tos=i.get('target_os', '')
    tdid=i.get('device_id', '')

    at=i.get('access_type','')

    if i.get('use_host','')=='yes':
       at='host'

    duoa=i.get('data_uoa','')
    if duoa=='':
       duoa=i.get('alias','')

    exc='no'
    if i.get('share',''):
        exc='yes'

    er=i.get('exchange_repo','')
    esr=i.get('exchange_subrepo','')

    dp='' # detect platform

    # Preliminary host detect
    os_tags=[]

    r=ck.get_os_ck({})
    if r['return']>0: return r

    if r['platform']=='win':
       os_tags=["windows","mingw"]
    else:
       os_tags=["linux"]

    # If not host target
    if at=='' and o=='con':
        tat=cfg['target_access_types']

        ck.out(line)

        r=ck.select({'title':'Select access type for your target machine: ',
                     'dict':tat})
        if r['return']>0: return r
        at=r['string']

    # If access_type is empty, quit
    if at=='':
        return {'return':1, 'error':'access type is not specified'}

    # Continue processing
    tags=[]
    extra_check={}
    prefix=''
    rtags=''
    if at!='':
       tags=tat[at]['tags']
       dp=tat[at]['detect_platform']
       extra_check=tat[at].get('extra_check',{})
       prefix=tat[at].get('alias_prefix','')
       rtags=tat[at].get('record_tags','')
       dos=''

    # Extra checks
    if tos=='':
        if 'android-with-arch' in tags:
            # Check preliminary Android parameters including arch + API to finalize detecton of the CK OS description
            if o=='con':
                ck.out(line)
                ck.out('Attempting to detect Android API and arch ...')
                ck.out('')

            ii={'action':'detect',
                'host_os':hos,
                'target_os':'android-32',
                'module_uoa':cfg['module_deps']['platform.cpu'],
                'out':oo}
            r=ck.access(ii)
            if r['return']>0: return r

            tdid=r['device_id']

            params=r['features']['os_misc'].get('adb_params',{})

            sdk=str(params.get('ro.build.version.sdk',''))
            abi=str(params.get('ro.product.cpu.abi',''))

            if sdk!='':
                if o=='con':
                   ck.out('')
                   ck.out('Android API: '+sdk)

                for q in range(0, len(tags)):
                    tags[q]+=',android-'+sdk

            if abi!='':
                if o=='con':
                   ck.out('')
                   ck.out('Android ABI: '+abi)

                if abi.startswith('arm64'):
                    dos='*-arm64'
                elif abi.startswith('arm'):
                    dos='*-arm'

    # Check tags and use host ones if empty
    if len(tags)==0 and len(os_tags)>0:
        tags=os_tags

    # Search target OS
    if tos=='':
        lst=[]

        for t in tags:
            ii={'action':'search',
                'module_uoa':cfg['module_deps']['os'],
                'data_uoa':dos,
                'tags':t}
            r=ck.access(ii)
            if r['return']>0: return r

            for q in r['lst']:
                lst.append(q)

        if len(lst)==0:
            return {'return':1, 'error':'no OS found for tags "'+str(tags)+'" and OS wildcard "'+dos+'"'}
        elif len(lst)==1:
            tos=lst[0]['data_uoa']
        else:
            ck.out(line)
            ck.out('Select most close OS and architecture on a target machine:')
            ck.out('')

            r=ck.select_uoa({'choices':lst})
            if r['return']>0: return r
            tos=r['choice']

    # Target OS should be finalized
    if tos=='':
        return {'return':1, 'error':'no target OS selected'}

    # Get user friend alias of OS
    if tos!='':
       r=ck.access({'action':'load',
                    'module_uoa':cfg['module_deps']['os'],
                    'data_uoa':tos})
       if r['return']>0: return r
       tos=r['data_uoa']
       tosd=r['dict']

    if o=='con':
        if tos!='':
            ck.out(line)
            ck.out('Selected target OS UOA:    '+tos)

        if tdid!='':
            ck.out('Selected target device ID: '+tdid)

    # Extra checks if needed
    dd={}
    files={}
    if len(extra_check)>0:
        ii=copy.deepcopy(extra_check)

        ii['out']=oo
        ii['device_id']=tdid

        r=ck.access(ii)
        if r['return']>0: return r

        files=r.get('files',{})
        dd['device_cfg']={'wa_config':r.get('cfg',{})}

    ########################################################## Additional questions for SSH or CK
    if at=='ssh' or at=='ck_node':
        if 'device_cfg' not in dd:
            dd['device_cfg']={}

        dx={}

        #####################
        ck.out('')
        r=ck.inp({'text':'Enter hostname (Enter for localhost):          '})

        host=r['string'].strip()
        if host=='': host='localhost'
        dx['host']=host

        #####################
        if at=='ssh':
            ck.out('')
            r=ck.inp({'text':'Enter host port if needed:                     '})

            port=r['string'].strip()
            dx['port']=port

            #####################
            ck.out('')
            r=ck.inp({'text':'Enter username (Enter for root):               '})

            username=r['string'].strip()
            if username=='': username='root'
            dx['username']=username

        else:
            ck.out('')
            r=ck.inp({'text':'Enter host port if needed (Enter for 3333):    '})

            port=r['string'].strip()
            if port=='': port='3333'
            dx['port']=port

        #####################
        ck.out('')
        r=ck.inp({'text':'Enter full path to public keyfile:             '})

        keyfile=r['string'].strip()
        dx['keyfile']=keyfile

        #####################
        path_to_files="tmp-ck"
        if at=='ck_node':
            ck.out('')
            r=ck.inp({'text':'Enter full path to files on a target:          '})

            path_to_files=r['string'].strip()
            dx['path_to_files']=path_to_files

        dd['device_cfg']['remote_params']=dx

        # Prepare OS update
        port1=''
        if port!='':
            port1=':'+port

        keyfile1=''

        uod={
             "remote": "yes",
             "remote_ssh":"yes",
             "remote_deinit": "",
             "remote_dir_sep": tosd.get('dir_sep',''),
             "remote_env_quotes_if_space": tosd.get('env_quotes_if_space',''),
             "remote_shell_end": "\""
            }

        if at=='ssh':
            port2=''
            port3=''

            if port!='':
                port2='-p '+port
                port3='-P '+port

            if keyfile!='':
                keyfile1='-i '+keyfile

            uod.update({
                 "remote_dir": path_to_files,
                 "remote_id": username+"@"+host+port1,
                 "remote_init": "ssh "+port2+" -l "+username+" "+host+" "+keyfile1+" \"echo remote_init...\"",
                 "remote_pull": "scp "+port3+" "+keyfile1+" "+username+"@"+host+":$#file1#$ \"$#file2#$\"",
                 "remote_push": "scp "+port3+" "+keyfile1+" \"$#file1#$\" "+username+"@"+host+":$#file2#$",
                 "remote_shell": "ssh "+port2+" -l "+username+" "+host+" "+keyfile1+" \""
                })

        else:
            if keyfile!='':
                keyfile1='--keyfile='+keyfile

            uod.update({
                 "remote_dir": "",
                 "remote_dir_full": path_to_files,
                 "remote_id": host+port1,
                 "remote_init": "ck shell crowdnode --url="+host+port1+" "+keyfile1+" --cmd=\"echo remote_init...\"",
                 "remote_pull": "ck pull crowdnode --url="+host+port1+" "+keyfile1+" --filename=$#file1#$ --filename2=\"$#file2#$\"",
                 "remote_push": "ck push crowdnode --url="+host+port1+" "+keyfile1+" --filename=$#file1#$ --filename2=\"$#file2#$\"",
                 "remote_shell": "ck shell crowdnode --url="+host+port1+" "+keyfile1+" --cmd=\""
                })

        tosd.update(uod)

        dd['device_cfg']['update_target_os_dict']=uod

    # Detect various parameters of the platform (to suggest platform name as well)
    pn=''
    rp={}
    if dp=='yes':
        if o=='con':
            ck.out(line)
            ck.out('Attempting to detect various parameters of your target machine ...')
            ck.out('')

        ii={'action':'detect',
            'host_os':hos,
            'target_os':tos,
            'target_os_dict':tosd,
            'device_id':tdid,
            'module_uoa':cfg['module_deps']['platform'],
            'exchange':exc,
            'exchange_repo':er,
            'exchange_subrepo':esr,
            'out':oo}
        rp=ck.access(ii)
        if rp['return']>0: return rp

        tdid=rp.get('device_id','')

        pn=rp.get('features',{}).get('platform',{}).get('name','')

    # Finalize machine meta
    dd.update({'host_os':hos,
               'target_os':tos,
               'device_id':tdid,
               'host_os_uoa':rp.get('host_os_uoa',''),
               'host_os_uid':rp.get('host_os_uid',''),
               'host_os_dict':rp.get('host_os_dict',{}),
               'target_os_uoa':rp.get('os_uoa',''),
               'target_os_uid':rp.get('os_uid',''),
               'target_os_dict':tosd,
               'access_type':at,
               'features':rp.get('features',{})})

    # Suggest platform name
    if duoa=='':
        if o=='con':
            ck.out(line)

        if pn!='' and o=='con':
            ck.out('Detected target machine name: '+pn)
            ck.out('')

        if at=='host':
            duoa='host'
        elif pn!='':
            duoa=pn.lower().replace(' ','-').replace('_','-').replace('(','-').replace(')','-').replace('"','-')

        if duoa!='' and prefix!='':
            duoa=prefix+duoa

        if o=='con':
            s='Enter an alias for your machine to be recorded in your CK local repo'

            if duoa!='':
                s+=' or press Enter for "'+duoa+'"'

            s+=' : '

            ck.out('')

            r=ck.inp({'text':s})
            x=r['string'].strip()

            if x!='': duoa=x

    # Check that alias is there
    if duoa=='':
        return {'return':1, 'error':'machine alias is not defined'}

    # Check if entry already exists
    ii={'action':'load',
        'module_uoa':work['self_module_uid'],
        'data_uoa':duoa}
    r=ck.access(ii)
    if r['return']>0 and r['return']!=16:
        return r

    if r['return']==0:
        renew=False

        s='CK entry "machine:'+duoa+'" already exists'
        if o=='con':
            ck.out('')

            r=ck.inp({'text':s+'. Renew (Y/n)? '})
            x=r['string'].strip().lower()

            if x=='' or x=='y' or x=='yes':
                renew=True
            else:
                return {'return':0}

        if not renew:
            return {'return':1, 'error':s}

    ii={'action':'update',
        'module_uoa':work['self_module_uid'],
        'data_uoa':duoa,
        'dict':dd,
        'tags':rtags,
        'substitute':'yes',
        'sort_keys':'yes'}
    r=ck.access(ii)
    if r['return']>0: return r

    duoa=r['data_uoa']
    duid=r['data_uid']

    p=r['path']

    if len(files)>0:
        for f in files:
            xcfg=files[f]
            pp=os.path.join(p,f)

            r=ck.save_text_file({'text_file':pp, 'string':xcfg})
            if r['return']>0: return r

    # Success
    if o=='con':
        ck.out(line)
        ck.out('Your target machine was successfully registered in CK with alias: '+duoa+' ('+duid+')')

    return {'return':0}

##############################################################################
# show registered target machines and their status

def show(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    o=i.get('out','')

    if o=='con':
       ck.out(line)
       ck.out('Checking machines ...')
       ck.out('')

    h='<center>\n'

    a=[]

    c='Registered target machines and their status:'

    h+='<h2>'+c+'</h2>\n'

    # Check host URL prefix and default module/action
    rx=ck.access({'action':'form_url_prefix',
                  'module_uoa':'wfe',
                  'host':i.get('host',''), 
                  'port':i.get('port',''), 
                  'template':i.get('template','')})
    if rx['return']>0: return rx
    url0=rx['url']
    template=rx['template']

    url=url0
    action=i.get('action','')
    muoa=i.get('module_uoa','')

    st=''

    url+='action=index&module_uoa=wfe&native_action='+action+'&'+'native_module_uoa='+muoa
    url1=url

    # List entries
    r=ck.access({'action':'search',
                 'module_uoa':work['self_module_uid'],
                 'add_meta':'yes'})
    if r['return']>0: return r

    lst=r['lst']

    h+='<table border="1" cellpadding="7" cellspacing="0">\n'

    h+='  <tr>\n'
    h+='   <td align="center"><b>CK alias</b></td>\n'
    h+='   <td align="center"><b>Real machine name</b></td>\n'
    h+='   <td align="center"><b>Native ID</b></td>\n'
    h+='   <td align="center"><b>Target OS name</b></td>\n'
    h+='   <td align="center"><b>OS UOA</b></td>\n'
    h+='   <td align="center"><b>CPUs</b></td>\n'
    h+='   <td align="center"><b>GPUs</b></td>\n'
    h+='   <td align="center"><b>GPGPUs</b></td>\n'
    h+='   <td align="center"><b>Status</b></td>\n'
    h+='  <tr>\n'

    c+='\n'
    for q in sorted(lst, key = lambda v: v['data_uoa']):
        duoa=q['data_uoa']
        duid=q['data_uid']

        d=q['meta']

        tdid=d.get('machine_id','')

        tos=d.get('target_os_uoa','')
        tos_uid=d.get('target_os_uid','')

        r=check({'data_uoa':duoa})
        if r['return']>0: return r

        connected=r['connected']

        at=d.get('access_type','')

        a.append({'data_uoa':duoa, 'data_uid':duid, 'connected':connected})

        # Prepare info
        if connected=='yes':
            ss=' style="background-color:#009f00;color:#ffffff"'
            sx='connected'
        else:
            ss=' style="background-color:#9f0000;color:#ffffff;"'
            sx='not found'

        h+='  <tr>\n'

        ft=d.get('features',{})
        rn=ft.get('platform',{}).get('name','')

        on=ft.get('os',{}).get('name','')

        cpus=''
        for q in ft.get('cpu_unique',[]):
            x=q.get('ck_cpu_name','')
            if x!='':
                if cpus!='': 
                    cpus+='<br>\n'
                cpus+=x

        gpu=ft.get('gpu',{}).get('name','')

        gpgpus=''

        # Prepare HTML
        c+='\n'
        c+=duoa+': '
        h+='   <td align="left"><a href="'+url0+'&wcid='+work['self_module_uid']+':'+duid+'">'+duoa+'</a></td>\n'

        h+='   <td align="center">'+rn+'</td>\n'

        h+='   <td align="center">'+tdid+'</td>\n'

        h+='   <td align="center">'+on+'</td>\n'

        h+='   <td align="center"><a href="'+url0+'&wcid='+cfg['module_deps']['os']+':'+tos_uid+'">'+tos+'</a></td>\n'

        h+='   <td align="center">'+cpus+'</td>\n'

        h+='   <td align="center">'+gpu+'</td>\n'

        h+='   <td align="center">'+gpgpus+'</td>\n'

        c+=sx
        h+='   <td align="center"'+ss+'>'+sx+'</td>\n'

        h+='  <tr>\n'

    h+='</table>\n'
    h+='</center>\n'

    if o=='con':
       ck.out(line)
       ck.out(c)

    return {'return':0, 'html':h, 'style':st, 'availability':a}

##############################################################################
# view machines in the browser

def browse(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    i['action']='start'
    i['cid']=''
    i['module_uoa']='web'
    i['browser']='yes'
    i['extra_url']='action=index&module_uoa=wfe&native_action=show&native_module_uoa=machine'
    i['template']=''

    return ck.access(i)

##############################################################################
# init machine and update input

def machine_init(i):
    """
    Input:  {
              (target) - target machine
              (input)  - input to update
              (check)  - if 'yes', check status and quit if not connected
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    ii=i.get('input',{})

    target=ii.get('target','')
    if target!='':
        # Check if connected
        if i.get('check','')=='yes':
            r=check({'data_uoa':target})
            if r['return']>0: return r
            if r['connected']!='yes':
               return {'return':1, 'error':'target machine "'+target+'" is not connected'}

        # Load machine entry
        r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':target})
        if r['return']>0: return r

        dd=r['dict']

        # Get main parameters
        host_os_uoa=dd.get('host_os_uoa','')
        target_os_uoa=dd.get('target_os_uoa','')
        target_device_id=dd.get('target_device_id','')

        at=dd.get('access_type','')
        ecfg=dd.get('device_cfg',{})

        # Update input (if undefined)
        if ii.get('target_os','')=='':
            ii['target_os']=target_os_uoa
        if ii.get('device_id','')=='':
            ii['device_id']=target_device_id
        if len(ii.get('device_cfg',{}))==0:
            ii['device_cfg']=ecfg
            ii['device_cfg']['access_type']=at

    return {'return':0}

##############################################################################
# check machine status (online/offline)

def check(i):
    """
    Input:  {
              data_uoa     - machine UOA
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              connected    - 'yes'/'no'
            }

    """

    o=i.get('out','')

    duoa=i['data_uoa']
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uid'],
                 'data_uoa':duoa})
    if r['return']>0: return r

    d=r['dict']

    device_cfg=d.get('device_cfg',{})

    hos=d.get('host_os_uoa','')

    tos=d.get('target_os_uoa','')
    tos_uid=d.get('target_os_uid','')

    tdid=d.get('target_device_id','')

    # Check if machine connected
    connected='yes'

    at=d.get('access_type','')

    if at=='host' or at=='wa_linux':
        connected='yes'
    else:
        # Check status of remote
        connected='no'

        if at=='android' or at=='wa_android' or at=='ssh' or at=='ck_node':
            # Attempt to get Android features 
            ii={'action':'detect',
                'module_uoa':cfg['module_deps']['platform.os'],
                'host_os':hos,
                'target_os':tos,
                'device_cfg':device_cfg,
                'device_id':tdid}
            r=ck.access(ii)

            if r['return']==0:
               connected='yes'

    if o=='con':
       if connected=='yes':
          ck.out('connected')
       else:
          ck.out('offline')

    return {'return':0, 'connected':connected}
