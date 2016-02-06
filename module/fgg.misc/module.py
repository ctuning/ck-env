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

    f1=i['file1']
    f2=i['file2']
    
    fo=i.get('file3','')
    if fo=='': fo=f1

    r=ck.load_json_file({'json_file':f1})
    if r['return']>0: return r
    d1=r['dict']

    r=ck.load_json_file({'json_file':f2})
    if r['return']>0: return r
    d2=r['dict']

    r=ck.merge_dicts({'dict1':d1, 'dict2':d2})
    if r['return']>0: return r
    d1=r['dict1']

    r=ck.save_json_to_file({'json_file':fo, 'dict':d1})
    if r['return']>0: return r

    return {'return':0}
