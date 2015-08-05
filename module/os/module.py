#
# Collective Knowledge (os)
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
# find close OS

def find_close(i):
    """
    Input:  {
              (os_uoa)     - load info from a given OS
            }

    Output: {
              return   - return code =  0

              platform - 'win' or 'linux'
              bits     - (str) 32 or 64

              os_uoa   - UOA of the most close OS
              os_uid   - UID of the most close OS
              os_dict  - meta of the most close OS
            }
    """

    r=ck.get_os_ck({})
    if r['return']>0: return r

    bits=r['bits']
    plat=r['platform']

    xos=i.get('os_uoa','')
    fc=i.get('find_close','')

    if xos=='':
       # Detect host platform
       # Search the most close OS
       ii={'action':'search',
           'module_uoa':work['self_module_uid'],
           'search_dict':{'ck_name':plat,
                          'bits':bits,
                          'generic':'yes',
                          'priority':'yes'},
           'internal':'yes'}

       # Adding extra tags to separate different Linux flavours such as Mac OS X:
       import sys
       pl=sys.platform

       if pl=='darwin':
          ii['tags']='macos'

       rx=ck.access(ii)
       if rx['return']>0: return rx

       lst=rx['lst']
       if len(lst)==0:
          return {'return':0, 'error':'most close platform was not found in CK'}

       pl=lst[0]

       xos=pl.get('data_uoa','')

    rr={'return':0, 'platform':plat, 'bits':bits}

    # Load OS
    if xos!='':
       r=ck.access({'action':'load',
                    'module_uoa':'os', 
                    'data_uoa':xos})
       if r['return']>0: return r

       os_uoa=r['data_uoa']
       os_uid=r['data_uid']

       dd=r['dict']

       rr['os_uoa']=os_uoa
       rr['os_uid']=os_uid
       rr['os_dict']=dd

    return rr
