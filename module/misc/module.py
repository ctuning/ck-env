#
# Collective Knowledge (Grigori's misc research functions)
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
# Replace string in file

def replace_string_in_file(i):
    """
    Input:  {
              file
              (file_out)  - if !='', use this file for output, otherwise overwrite original one!
              string      - string to replace
              replacement - replacement string
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              (updated)    - if 'yes', files was updated
            }

    """

    import copy

    o=i.get('out','')

    fin=i['file']
    s1=i['string']
    s2=i['replacement']

    fout=i.get('file_out','')
    if fout=='': fout=fin

    rx=ck.load_text_file({'text_file':fin})
    if rx['return']>0: return rx

    s=rx['string']
    sx=s.replace(s1,s2)

    r={'return':0, 'updated':'no'}

    if s!=sx or fin!=fout:
       r=ck.save_text_file({'text_file':fout, 'string':sx})
       r['updated']='yes'

    return r

##############################################################################
# updating json file

def refresh_json(i):
    """
    Input:  {
              json_file     - file with json
              (output_file) - if !='' use this file for output instead of rewriting original file
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    jf=i['json_file']

    of=i.get('output_file','')
    if of=='': of=jf

    r=ck.load_json_file({'json_file':jf})
    if r['return']>0: return r

    d=r['dict']

    return ck.save_json_to_file({'json_file':of, 'dict':d, 'sort_keys':'yes'})

##############################################################################
# process all files recursively using some action

def process_all_files_recursively(i):
    """
    Input:  {
               (path)     - starting path (or current)
               (pattern)  - file pattern
               (cmd)      - perform action with a file

               (ck)       - call CK access
               (file_key) - substitute this key in 'ck' with file name with full path
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    o=i.get('out','')

    p=i.get('path','')
    if p=='':
       p=os.getcwd()

    cka=i.get('ck',{})
    fk=i.get('file_key','')

    pat=i.get('pattern','')

    if o=='con':
       ck.out('')
       x=''
       if pat!='': x=' ('+pat+')'
       ck.out('Obtaining list of all files'+x+'. May take some time ...')

    r=ck.list_all_files({'path':p, 'pattern':pat, 'all':'yes'})
    if r['return']>0: return r

    lst=r['list']

    for qq in lst:
        if p=='': q=qq
        else:     q=os.path.join(p,qq)

        if len(cka)>0:
           if fk!='':
              cka[fk]=q

           if o=='con':
              ck.out('  '+q)

           r=ck.access(cka)
           if r['return']>0: return r

    return {'return':0, 'list':lst}

##############################################################################
# merge dictionaries in 2 files

def merge_dicts(i):
    """
    Input:  {
              file1   - dict1
              file2   - dict2
              (file3) - output to this file. If empty use file1
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    f1=i.get('file1','')
    f2=i.get('file2','')

    if f1=='' or f2=='':
       return {'return':1, 'error':'--file1 and --file2 should be specified'}

    fo=i.get('file3','')
    if fo=='': fo=f1

    r=ck.load_json_file({'json_file':f1})
    if r['return']>0: return r
    d1=r['dict']

    r=ck.load_json_file({'json_file':f2})
    if r['return']>0: return r
    d2=r['dict']

    if type(d1)==list and type(d2)==list:
       for q in d2:
           d1.append(q)
    else:
       r=ck.merge_dicts({'dict1':d1, 'dict2':d2})
       if r['return']>0: return r
       d1=r['dict1']

    r=ck.save_json_to_file({'json_file':fo, 'dict':d1})
    if r['return']>0: return r

    return {'return':0}

##############################################################################
# sort JSON file

def sort_json_file(i):
    """
    Input:  {
              json_file     - file with json
              (output_file) - if !='' use this file for output instead of rewriting original file
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    return refresh_json(i)

##############################################################################
# add key to meta/files of different entries

def add_key(i):
    """
    Input:  {
              data            - CID of entries to update (can be wild cards)
              (tags)          - prune entries by tags

              key             - key in flat format
              value           - value

              (ignore_update) - ignore update info in entries
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    o=i.get('out','')

    data=i.get('data','')
    if data=='':
       return {'return':1, 'error':'"data" is not defined'}

    tags=i.get('tags','')

    key=i.get('key','')
    if key=='':
       return {'return':1, 'error':'"key" is not defined'}

    value=i.get('value','')
    if value=='':
       return {'return':1, 'error':'"value" is not defined'}

    iu=i.get('ignore_update','')

    # Search entries
    r=ck.access({'action':'search',
                 'cid':data,
                 'tags':tags})
    if r['return']>0: return r
    lst=r['lst']

    llst=len(lst)

    if llst>0 and o=='con':
       ck.out('Updating '+str(llst)+' entries ...')
       ck.out('')

    # Iterate over entries
    for l in lst:
        ruid=l['repo_uid']
        ruoa=l['repo_uoa']
        muid=l['module_uid']
        muoa=l['module_uoa']
        duid=l['data_uid']
        duoa=l['data_uoa']

        if o=='con':
           ck.out('* '+ruoa+':'+muoa+':'+duoa)

        # Load meta
        r=ck.access({'action':'load',
                     'repo_uoa':ruid,
                     'module_uoa':muid,
                     'data_uoa':duid})
        if r['return']>0: return r
        d=r['dict']

        # Updating dict
        r=ck.set_by_flat_key({'dict':d,
                              'key':key,
                              'value':value})
        if r['return']>0: return r

        # Store meta
        r=ck.access({'action':'update',
                     'repo_uoa':ruid,
                     'module_uoa':muid,
                     'data_uoa':duid,
                     'dict':d,
                     'substitute':'yes',
                     'ignore_update':iu})
        if r['return']>0: return r

    return {'return':0}

##############################################################################
# internal file to ignore files/directories from templates

def prepare_entry_template_ignore_files(dr, files):
    lst=['.cm','tmp']
    return lst

##############################################################################
# prepare template for a given entry
# (trying to unify templates for CK when adding program, soft, package, program, dataset, etc)

def prepare_entry_template(i):
    """
    Input:  {
              original_module_uoa - add template for this original module 
              (template)          - force using this template
              (skip_custom_note)  - if 'yes', do not print note about customization at the end

              all params from "ck add" function
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import shutil

    o=i.get('out','')
    oo=''
    if o=='con': oo=o

    omuoa=i.get('original_module_uoa','')
    ruoa=i.get('repo_uoa','')
    duoa=i.get('data_uoa','')

    # Search templates
    tuoa=i.get('template','')
    truoa=i.get('template_repo','')

    if tuoa=='':
       lst=[{'data_uid':'', 'data_uoa':'', 'repo_uid':'', 'info':{'data_name':'Empty entry'}, 'meta':{'sort':9999}}] # Add it to the end

       if tuoa=='':
          if oo=='con':
             ck.out('Searching for templates ...')

          ii={'action':'search',
              'module_uoa':omuoa,
              'data_uoa':tuoa,
              'add_info':'yes',
              'search_dict':{'template':'yes'}}
          r=ck.access(ii)
          if r['return']>0: return r

          lst+=r['lst']

       if len(lst)==1:
          c=lst[0]

       # Make selection
       if oo=='con' and len(lst)>1:
          ck.out('')

          r=select_uoa({'text':'Select template for the new entry', 
                        'choices':lst})
          if r['return']>0: return r

          c=r['choice']

          ck.out('')

       tuoa=c['data_uid']
       truoa=c['repo_uid']

    d=i.get('dict',{})

    if tuoa!='':
       # Attempt to load entry
       ii={'action':'load',
           'module_uoa':omuoa,
           'data_uoa':tuoa,
           'repo_uoa':truoa}
       r=ck.access(ii)
       if r['return']>0: return r

       p=os.path.realpath(r['path'])

       d.update(r['dict'])

    i['action']='add'
    i['module_uoa']=omuoa

    i['common_func']='yes'
    i['sort_keys']='yes'

    i['dict']=d
    
    r=ck.access(i)
    if r['return']>0: return r

    pnew=r['path']

    # Copy files to a new entry if template
    if tuoa!='':
       d=os.listdir(p)
       for f in d:
           if f!='.cm' and not f.endswith('.pyc') and 'tmp' not in f:
              porig2=os.path.join(p,f)
              pnew2=os.path.join(pnew,f)

              try:

                 if os.path.isdir(porig2):
                    shutil.copytree(porig2, pnew2, ignore=shutil.ignore_patterns('.cm', '*tmp*', '*.pyc'))
                 else:
                    shutil.copyfile(porig2, pnew2)

              except IOError as e: 
                 return {'return':1, 'error':'problem copying files from template ('+str(e)+')'}

    # Print info about customization
    if i.get('skip_custom_note', '')!='yes' and oo=='con':
       ck.out('')
       ck.out('You can continue customizing this entry (tags, dependencies, etc):')
       ck.out('')
       ck.out(' * JSON meta:   '+os.path.join(pnew, ck.cfg['subdir_ck_ext'], ck.cfg['file_meta']))
       ck.out(' * Other files: '+pnew)

    return r

##############################################################################
# Universal UOA selector (improved version forked 
# from ck-autotuning:module:choice and ck.kernel)

def select_uoa(i):
    """
    Input:  {
              choices      - list from search function
              (text)       - selection text
              (skip_enter) - if 'yes', do not select 0 when user presses Enter
              (skip_sort)  - if 'yes', do not sort array
            }

    Output: {
              return  - return code =  0, if successful
                                    >  0, if error
              (error) - error text if return > 0
              choice  - {dict of selection from lst}
            }

    """

    se=i.get('skip_enter','')

    lst=i.get('choices',[])

    # Prepare data_name and then data_uoa

    if i.get('skip_sort','')!='yes':
       slst=sorted(lst, key=lambda v: (v.get('meta',{}).get('sort',0), v.get('info',{}).get('data_name',''), v['data_uoa']))
    else:
       slst=lst

    array={}
    n=0

    for x in slst:
        sn=str(n)
        array[sn]=x

        duoa=x['data_uoa']
        name=x.get('info',{}).get('data_name','')
        if name=='': name=duoa

        s=sn+') '+name
        if duoa!='': s+=' (--template='+duoa+')'

        ck.out(s)

        n+=1

    ck.out('')

    text=i.get('text','')
    if text=='': text='Select UOA'

    s=text
    if se!='yes': s+=' (or press Enter for 0)'
    s+=': '

    rx=ck.inp({'text':s})
    y=rx['string'].strip()

    if y=='' and se!='yes': y='0' 

    if y not in array:
       return {'return':1, 'error':'number is not recognized'}

    return {'return':0, 'choice':array[y]}
