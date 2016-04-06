#
# Collective Knowledge (individual environment - detect soft)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

##############################################################################
# setup environment setup

import sys
if sys.version_info[0]>2:
   def raw_input(i):
       return input(i)

def setup(i):
    """
    Input:  {

              ck_kernel    - CK kernel

              cfg          - dict of the soft entry

              interactive  - if 'yes', ask questions
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    import datetime
    import time

    # Get variables
    s=''

    ck=i['ck_kernel']

    iv=i.get('interactive','')

    env=i.get('env',{})
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})
    tags=i.get('tags',[])
    cus=i.get('customize',{})

    host_d=i.get('host_os_dict',{})
    target_d=i.get('target_os_dict',{})
    win=target_d.get('windows_base','')
    winh=host_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    pi=''

    if win=='yes':
       return {'return':1, 'error':'this soft description does not support Windows'}

    if remote=='yes':
       return {'return':1, 'error':'this soft description does not support remote target'}

    # Searching for lib in main places ...
    lst=[]

    dirs=['/usr', '/usr/lib', '/usr/local', '/usr/local/lib64', '/usr/local/lib', '/usr/local/lib32']

    # Check extra dirs in /etc/OpenCL/vendors
    r=ck.list_all_files({'path':'/etc/OpenCL/vendors', 'pattern':'*.icd', 'all':'yes', 
                         'ignore_symb_dirs':'yes', 'add_path':'yes'})
    if r['return']>0: return r
    icd=r['list']

    for q in icd:
        px=icd[q]['path']
        pf=os.path.join(px,q)
        if os.path.isfile(pf):
           r=ck.load_text_file({'text_file':pf, 'split_to_list':'yes'})
           if r['return']>0: return r

           xlst=r['lst']
           for k in xlst:
               py=os.path.dirname(os.path.dirname(k))
               if os.path.isdir(py):
                  dirs.append(py)

    # Search for a given soft
    pincludes=[]

    pinc=''
    for p in dirs:
        for pe in ['','x86_64-linux-gnu', 'beignet', 'x86_64-linux-gnu/beignet']: 
            for p2 in ['','lib64', 'lib', 'lib32']: 
                for fn in ['libOpenCL.so', 'libcl.so', 'libmali.so']:
                    # Check include
                    pq=os.path.join(p,pe,'include','CL','opencl.h')
                    if os.path.isfile(pq): pinc=pq

                    # Check lib
                    px=os.path.join(p,pe,p2,fn)
                    if os.path.isfile(px):
                       # Check that not found yet
                       found=False

                       for k in lst:
                           if k['path_full']==px:
                              found=True
                              break

                       if not found:


#static lib


                          g={'path':p, 'path_extra':pe, 'path2':p2, 'path_full':px, 'file':fn, 'path_include':pinc}

                          tm=os.path.getmtime(px)
                          dtm=datetime.datetime.fromtimestamp(tm).isoformat()
                          g['iso_datetime']=dtm

                          lst.append(g)

    if len(lst)==0:
       return {'return':16, 'error':'software not found'}

    il=0
    if len(lst)>1:
       if iv=='yes':
          il=0

          if iv=='yes':
             ck.out('')

             sel={}
             iq=0
             for q in lst:
                 sel[str(iq)]={'name':q['path_full']+' ('+q['iso_datetime'].replace('T',' ')+')'}
                 iq+=1

             rx=ck.select({'dict':sel, 'title':'More than one software found, select from path or press Enter to select 0:'})
             if rx['return']>0: return rx

             il=int(rx['string'])

# check version from .so.1.2




    ll=lst[il]
    pf=ll['path_full']
    pi1=ll['path']
    pl=os.path.dirname(pf)
    pi=os.path.dirname(pi1)
    pie=ll['path_extra']
    fn=ll['file']
    fns=ll.get('file1','')
    if fns=='': fns=fn
    pinc=ll.get('path_include','')

    # Pre-set dictionary to register found software in CK (ck setup soft:...)
    cus['path_install']=pi

    cus['path_check']=pf # to check if still there ...

    cus['tool_dir_extra']=pie
    cus['tool_dir_extra_configured']='yes'

    cus['path_lib']=pl
    cus['dynamic_lib']=fn
    cus['static_lib']=fns

    if pinc!='':
       cus['path_include']=os.path.dirname(os.path.dirname(pinc))
       cus['include_name']='CL/opencl.h'

    return {'return':0, 'path_install':pi, 'cus':cus}
