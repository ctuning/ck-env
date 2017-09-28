#
# Collective Knowledge (script)
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
# run script

def run(i):
    """
    Input:  {
              data_uoa            - data UOA of the script entry
              (repo_uoa)          - repo UOA of the script entry
              (script_module_uoa) - module UOA of the script entry

              name                - subscript name (from entry desc - will be called via shell)
              (params)            - pass params to CMD

                or

              (code)              - Python script name (without .py)
              (func)              - Python func in this script
              (dict)              - dict to pass to script

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

    code=i.get('code','')
    func=i.get('func','')

    # Loading entry
    rx=ck.access({'action':'load',
                  'module_uoa': muoa,
                  'data_uoa':duoa})
    if rx['return']>0: return rx
    d=rx['dict']
    p=rx['path']

    if code!='' and func!='':
       cs=None
       r=ck.load_module_from_path({'path':p, 'module_code_name':code, 'skip_init':'yes'})
       if r['return']>0: return r

       cs=r.get('code', None)
       if cs==None:
          return {'return':1, 'error':'no python code found'}

       script_func=getattr(cs, func)
       if script_func==None:
          return {'return':1, 'error':'function '+func+' not found in python script '+code}

       # Call customized script
       ii=i.get('dict',{})
       ii['ck_kernel']=ck

       rr=script_func(ii)
       if rr['return']>0:
          return {'return':1, 'error':'script failed ('+rx['error']+')'}

       rr['return_code']=0

    else:
       ss=d.get('sub_scripts',{})

       xs=ss.get(name,{})

       if len(xs)==0:
          return {'return':1, 'error':'subscript "'+name+'" is not found in entry "'+duoa+'"'}

       cmd=xs.get('cmd','')

       p1=p+os.path.sep

       cmd=cmd.replace('$#ck_path#$', p1)+' '+params

       rx=os.system(cmd)

       rr={'return':0, 'return_code':rx}

    return rr
