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

    import sys
    import shutil

    o=i.get('out','')

    fin=i['file']
    s1=i['string']
    s2=i['replacement']

    fout=i.get('file_out','')
    if fout=='': fout=fin

    rx=ck.load_text_file({'text_file':fin})
    if rx['return']>0: return rx

    s=rx['string']
    s1=rx['string'].replace(s1,s2)

    r={'return':0, 'updated':'no'}

    if s!=s1 or fin!=fout:
       r=ck.save_text_file({'text_file':fout, 'string':s})
       r['updated']='yes'

    return r