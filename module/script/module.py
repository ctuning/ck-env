#
# Collective Knowledge (script)
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
# run script

def run(i):
    """
    Input:  {
              data_uoa            - data UOA of the script entry
              (repo_uoa)          - repo UOA of the script entry
              (script_module_uoa) - module UOA of the script entry
              name                - subscript name
              (params)            - pass params to CMD
            }

    Output: {
              return        - return code =  0, if successful
                                          >  0, if error
              (error)       - error text if return > 0

              (return_code) - script's return code
            }

    """

    import os

    ruoa=i.get('repo_uoa','')
    muoa=i.get('script_module_uoa','')
    if muoa=='': muoa=work['self_module_uoa']
    duoa=i.get('data_uoa','')

    name=i.get('name','')

    params=i.get('params','')

    # Loading entry
    rx=ck.access({'action':'load',
                  'module_uoa': muoa,
                  'data_uoa':duoa})
    if rx['return']>0: return rx
    d=rx['dict']
    p=rx['path']

    ss=d.get('sub_scripts',{})

    xs=ss.get(name,{})

    if len(xs)==0:
       return {'return':1, 'error':'subscript "'+name+'" is not found in entry "'+duoa+'"'}

    cmd=xs.get('cmd','')

    p1=p+os.path.sep

    cmd=cmd.replace('$#ck_path#$', p1)+' '+params

    rx=os.system(cmd)

    return {'return':0, 'return_code':rx}
