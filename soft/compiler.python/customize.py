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
               if os.path.isdir(qq) and q.lower().startswith('python'):
                  dr.append(qq)

    return {'return':0}

##############################################################################
# limit directories 

def limit(i):

    dr=i.get('list',[])
    drx=[]

    for q in dr:
        if q.find('X11')<0:
           drx.append(q)

    return {'return':0, 'list':drx}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip()
        if q!='' and q.startswith('Python ') and len(q)>6:
           ver=q[7:]

           j=ver.find(' ::')
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

    host_d=i.get('host_os_dict',{})
    winh=host_d.get('windows_base','')

    fp=cus.get('full_path','')

    ep=cus.get('env_prefix','')
    p1=''
    if ep!='' and fp!='':
       p1=os.path.dirname(fp)
       p2=os.path.dirname(p1)

       env[ep]=p2
       env[ep+'_FILE']=fp
       env[ep+'_BIN']=p1

    if p1!='':
       ############################################################
       if winh=='yes':
          s+='\nset PATH='+p1+';'+p1+'\\Scripts;%PATH%\n\n'
       else:
          s+='\nexport PATH='+p1+':'+p1+'/Scripts:$PATH\n\n'

    return {'return':0, 'bat':s}
