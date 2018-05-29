#
# Collective Knowledge (artifact description (reproducibility, ACM meta, etc))
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
def recursive_repos(i):

    import os

    repo=i['repo']
    repo_deps=i.get('repo_deps',[])
    level=i.get('level','')

    # Load repo
    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['repo'],
                 'data_uoa':repo})
    if r['return']>0: return r

    d=r['dict']

    # Note that sometimes we update .ckr.json while CK keeps old deps cached
    p=d.get('path','')
    p1=os.path.join(p, ck.cfg['repo_file'])
    if os.path.isfile(p1):
       r=ck.load_json_file({'json_file':p1})
       if r['return']==0:
          d=r['dict'].get('dict',{})
    
    rd=d.get('repo_deps',{})

#    print (level+repo)

    for q in rd:
        drepo=q['repo_uoa']

        repo_deps.append(drepo)

        r=recursive_repos({'repo':drepo, 'repo_deps':repo_deps, 'level':level+'   '})
        if r['return']>0: return r

    return {'return':0, 'repo_deps':repo_deps}


##############################################################################
# prepare artifact snapshot

def snapshot(i):
    """
    Input:  {
              repo   - which repo to snapshot with all deps
              (date) - use this date (YYYYMMDD) instead of current one
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import platform
    import zipfile

    o=i.get('out','')

    repo=i.get('repo','')
    if repo=='':
       return {'return':1, 'error': '"repo" to snapshot is not defined'}

    # Preparing tmp directory where to zip repos and add scripts ...
    curdir0=os.getcwd()

    ptmp=os.path.join(curdir0, 'tmp')

    if os.path.isdir(ptmp):
       r=ck.inp({'text':'Directory "'+ptmp+'" exists. Delete (Y/n)?'})
       if r['return']>0: return r

       ck.out('')

       x=r['string'].strip().lower()
       if x=='' or x=='y' or x=='yes': 
          import shutil
          shutil.rmtree(ptmp)

    if not os.path.isdir(ptmp):
       os.makedirs(ptmp)

    os.chdir(ptmp)

    curdir=os.getcwd()

    # Checking repo deps
    if o=='con':
       ck.out('Checking dependencies on other repos ...')

    r=recursive_repos({'repo':repo})
    if r['return']>0: return r

    # Removing redundant
    final_repo_deps=[]
    for q in reversed(r['repo_deps']):
        if q not in final_repo_deps:
           final_repo_deps.append(q)

    final_repo_deps.append(repo)

    if o=='con':
       ck.out('')
       for q in final_repo_deps:
           ck.out(' * '+q)

       ck.out('')
       ck.out('Collecting revisions, can take some time ...')
       ck.out('')

    r=ck.reload_repo_cache({}) # Ignore errors

    pp=[]
    pp2={}
    il=0

    for repo in final_repo_deps:
        # Reload repo to get UID
        r=ck.access({'action':'load',
                     'module_uoa':cfg['module_deps']['repo'],
                     'data_uoa':repo})
        if r['return']>0: return r

        ruid=r['data_uid']

        if ruid not in ck.cache_repo_info:
           return {'return':1, 'error':'"'+q+'" repo is not in cache - strange!'}

        # Get repo info
        qq=ck.cache_repo_info[ruid]

        d=qq['dict']

        t=d.get('shared','')

        if t!='':
           duoa=qq['data_uoa']

           if len(duoa)>il: il=len(duoa)

           p=d.get('path','')
           url=d.get('url','')

           branch=''
           checkout=''

           if os.path.isdir(p):
              # Detect status
              os.chdir(p)

              # Get current branch
              r=ck.run_and_get_stdout({'cmd':['git','rev-parse','--abbrev-ref','HEAD']})
              if r['return']==0 and r['return_code']==0: 
                 branch=r['stdout'].strip()

              # Get current checkout
              r=ck.run_and_get_stdout({'cmd':['git','rev-parse','--short','HEAD']})
              if r['return']==0 and r['return_code']==0: 
                 checkout=r['stdout'].strip()

           x={'branch':branch, 'checkout':checkout, 'path':p, 'type':t, 'url':url, 'data_uoa':duoa}
           pp.append(x)
           pp2[duoa]=x

    # Print
    for q in pp:
        name=q['data_uoa']

        x=' * '+name+' '*(il-len(name))

        branch=q.get('branch','')
        checkout=q.get('checkout','')
        url=q.get('url','')

        if branch!='' or checkout!='' or url!='':
           x+=' ( '+branch+' ; '+checkout+' ; '+url+' )'

        ck.out(x)

    os.chdir(curdir)

    # Archiving
    if o=='con':
       ck.out('')
       ck.out('Archiving ...')

    # Add some dirs and files to ignore
    for q in ['__pycache__', 'tmp', 'module.pyc', 'customize.pyc']:
        if q not in ck.cfg['ignore_directories_when_archive_repo']:
           ck.cfg['ignore_directories_when_archive_repo'].append(q)

    # Get current date in YYYYMMDD
    date=i.get('date','')

    if date=='':
       r=ck.get_current_date_time({})
       if r['return']>0: return r

       a=r['array']

       a1=str(a['date_year'])

       a2=str(a['date_month'])
       a2='0'*(2-len(a2))+a2

       a3=str(a['date_day'])
       a3='0'*(2-len(a3))+a3

       date=a1+a2+a3

    zips=[]
    for repo in final_repo_deps:
        if o=='con':
           ck.out('')
           ck.out(' * '+repo)
           ck.out('')

        an='ckr-'+repo

        if pp2[repo].get('branch','')!='':
           an+='--'+pp2[repo]['branch']

        if pp2[repo].get('checkout','')!='':
           an+='--'+pp2[repo]['checkout']

        an+='.zip'

        zips.append(an)

        r=ck.access({'action':'zip',
                     'module_uoa':cfg['module_deps']['repo'],
                     'data_uoa':repo,
                     'archive_name':an,
                     'overwrite':'yes',
                     'out':o})
        if r['return']>0: return r

    # Print sequence of adding CK repos (for self-sustainable virtual CK artifact)
    if o=='con':
       ck.out('')

       for z in zips:
           ck.out('ck add repo --zip='+z)

    # Cloning CK master
    if o=='con':
       ck.out('')
       ck.out('Cloning latest CK version ...')
       ck.out('')

    os.system('git clone https://github.com/ctuning/ck ck-master')

    # Prepare scripts
    if o=='con':
       ck.out('')
       ck.out('Preparing scripts ...')

    f1=cfg['bat_prepare_virtual_ck']
    f2=cfg['bat_start_virtual_ck']

    if platform.system().lower().startswith('win'): # pragma: no cover
       f1+='.bat'
       f2+='.bat'

       s='set PATH=%~dp0\\ck-master\\bin;%PATH%\n'
       s+='set PYTHONPATH=%~dp0\\ck-master;%PYTHONPATH%\n'
       s+='\n'
       s+='set CK_REPOS=%~dp0\\CK\n'
       s+='set CK_TOOLS=%~dp0\\CK-TOOLS\n'
       s+='\n'

       s1=s+'mkdir %CK_REPOS%\n'
       s1+='mkdir %CK_TOOLS%\n'
       s1+='\n'

       s2=s+'rem uncomment next line to install tools to CK env entries rather than CK_TOOLS directory\n'
       s2+='rem ck set kernel var.install_to_env=yes\n'
       s2+='\n'

       s2+='call ck ls repo\n\n'
       s2+='cmd\n'

       s3='call '

    else:
       f1+='.sh'
       f2+='.sh'

       s='#! /bin/bash\n'
       s+='\n'
       s+='export PATH=$PWD/ck-master/bin:$PATH\n'
       s+='export PYTHONPATH=$PWD/ck-master:$PYTHONPATH\n'
       s+='\n'
       s+='export CK_REPOS=$PWD/CK\n'
       s+='export CK_TOOLS=$PWD/CK-TOOLS\n'
       s+='\n'

       s1=s+'mkdir ${CK_REPOS}\n'
       s1+='mkdir ${CK_TOOLS}\n'
       s1+='\n'

       s2=s+'# uncomment next line to install tools to CK env entries rather than CK_TOOLS directory\n'
       s2+='# ck set kernel var.install_to_env=yes\n'
       s2+='\n'

       s2+='ck ls repo\n\n'
       s2+='bash\n'

       s3=''

    # preparing unzip
    for z in zips:
        s1+=s3+'ck add repo --zip='+z+'\n'

    # Recording scripts
    r=ck.save_text_file({'text_file':f1, 'string':s1})
    if r['return']>0: return r
    r=ck.save_text_file({'text_file':f2, 'string':s2})
    if r['return']>0: return r

    # If non-Windows, set 755
    if not platform.system().lower().startswith('win'): # pragma: no cover
       os.system('chmod 755 '+f1)
       os.system('chmod 755 '+f2)

    # Generating final zip pack
    fname='ck-artifacts-'+date+'.zip'

    # Write archive
    if o=='con':
       ck.out('')
       ck.out('Recording '+fname+' ...')

    r=ck.list_all_files({'path':'.', 'all':'yes'})
    if r['return']>0: return r

    flx=r['list']

    try:
       f=open(os.path.join(curdir0,fname), 'wb')
       z=zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)

       for fn in flx:
           z.write(fn, fn, zipfile.ZIP_DEFLATED)

       # ck-install.json
       z.close()
       f.close()

    except Exception as e:
       return {'return':1, 'error':'failed to prepare CK artifact collections ('+format(e)+')'}

    return {'return':0}
