#
# Collective Knowledge (module providing API to communicate with various ck-crowdnodes ...)
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
import os

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
# push file to ck-crowdnode

def push(i):
    """
    Input:  {
              (url)      - URL to ck-crowdnode (http://localhost:3333 by default)
              (keyfile)  - path to key

              (filename) - local file to push to crowd-node

              (extra_path)          - extra path inside entry (create if doesn't exist)
              (archive)             - if 'yes' push to entry and unzip ...
              (overwrite)           - if 'yes', overwrite files
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    o=i.get('out','')

    url=i.get('hostname','')
    if url=='': url='http://localhost:3333'

    keyfile=i.get('keyfile','')
    key=''
    if keyfile!='':
        # Load keyfile
        r=ck.load_text_file({'text_file':keyfile})
        if r['return']>0: return r
        key=r['string'].strip()

    fn=i.get('filename','')
    if fn=='' or not os.path.isfile(fn):
        return {'return':1, 'error':'file '+fn+' not found'}

    ii={'action':'push',
        'remote_server_url':url,
        'secretkey':key,
        'extra_path':i.get('extra_path',''),
        'filename':fn}
    return ck.access(ii)

##############################################################################
# pull file from ck-crowdnode

def pull(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    exit(1)


    return {'return':0}

##############################################################################
# execute command on ck-crowdnode

def shell(i):
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

    url=i.get('hostname','')
    if url=='': url='http://localhost:3333'

    keyfile=i.get('keyfile','')
    key=''
    if keyfile!='':
        # Load keyfile
        r=ck.load_text_file({'text_file':keyfile})
        if r['return']>0: return r
        key=r['string'].strip()

    cmd=i.get('cmd','').strip()
    if cmd=='':
        return {'return':1, 'error':'cmd is not specified'}

    ii={'action':'shell',
        'remote_server_url':url,
        'secretkey':key,
        'cmd':cmd,
        'out':''}
    r=ck.access(ii)
    if r['return']>0: return r

    if o=='con':
        so=r.get('stdout','')
        se=r.get('stderr','')

        if type(so)==bytes:
            so=so.decode()

        ck.out(so)


    return r
