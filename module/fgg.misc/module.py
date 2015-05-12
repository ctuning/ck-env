#
# Collective Knowledge (Grigori's misc research functions)
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
