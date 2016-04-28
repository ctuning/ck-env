#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

##############################################################################
# customize directories to automatically find and register software

def dirs(i):
    import os

    dr=i.get('dirs',[])

    ck_os_name=i.get('host_os_dict',{}).get('ck_name','')
    if ck_os_name=='win':

       for px in ['C:\\', 'D:\\']:
           x=[]
           try:
              x=os.listdir(px)
           except:
              pass

           for q in x:
               qq=os.path.join(px,q)
               if os.path.isdir(qq) and q.lower().startswith('php'):
                  dr.append(qq)

    return {'return':0}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip()
        if q!='' and q.lower().startswith('php ') and len(q)>4:
           ver=q[4:]

           j=ver.find(' ')
           if j>0:
              ver=ver[:j]   
           break

    return {'return':0, 'version':ver}

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    import os

    # Get variables
    ck=i['ck_kernel']
    s=''

    cus=i['customize']
    env=i['env']

    fp=cus.get('full_path','')

    ep=cus.get('env_prefix','')
    if ep!='' and fp!='':
       p1=os.path.dirname(fp)
       p2=os.path.dirname(p1)

       env[ep]=p1
       env[ep+'_BIN']=p1

    return {'return':0, 'bat':s}
