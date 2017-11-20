#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os

##############################################################################
# customize directories to automatically find and register software

def dirs(i):

    hosd=i.get('host_os_dict',{})
    tosd=i.get('target_os_dict',{})

    phosd=hosd.get('ck_name','')
    hbits=hosd.get('bits','')

    ptosd=tosd.get('ck_name','')

    lst=i['dirs']
    dirs=lst

    if ptosd=='win':
       dirs=[]

       dirs.append("C:\\Intel\\OpenCL")
       dirs.append("D:\\Intel\\OpenCL")

       for p in lst:
           dirs.append(os.path.join(p, 'NVIDIA GPU Computing Toolkit\\CUDA'))
           dirs.append(os.path.join(p, 'Intel\\OpenCL SDK'))
           dirs.append(os.path.join(p, 'AMD APP SDK'))

    return {'return':0, 'dirs':dirs}

##############################################################################
# limit directories 

def limit(i):

    ck=i['ck_kernel']

    hosd=i.get('host_os_dict',{})
    tosd=i.get('target_os_dict',{})

    phosd=hosd.get('ck_name','')
    ptosd=tosd.get('ck_name','')
    hbits=hosd.get('bits','')
    tbits=tosd.get('bits','')

    remote=tosd.get('remote','')

    prebuilt=''
    if ptosd=='win':
       if hbits=='64':
          prebuilt='windows-x86_64'
       else:
          prebuilt='windows-x86'

    dr=i.get('list',[])
    drx=[]

    for q in dr:
        if phosd=='win':
           if q.find('\\src\\')<0 and q.find('/src/')<0:
              if tbits=='32' and q.find('x64')<0 and q.find('_64')<0:
                drx.append(q)
              elif tbits=='64' and (q.find('x64')>=0 or q.find('_64')>=0):
                 drx.append(q)
        else:
           add=True
           if remote!='yes':
              if q.find('android')>0:
                 add=False
           if add:
              drx.append(q)

    # Check extra dirs in vendors
    if phosd=='linux':
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
                  if os.path.isfile(k):
                     if k not in drx:
                        drx.append(k)

    skip_sort='no'
    # Check if nvidia and x86_64 present, then move x86_64 up 
    # (since Nvidia has only partial support for all OpenCL versions
    # and for example Caffe often breaks)

    drx1=[]
    drx2=[]
    drx3=[]
    for q in drx:
        if ('i386' in q or 'lib32' in q) and tbits=='64':
           continue

        if 'x86_64-' in q:
           drx1.append(q)
        elif 'cuda' in q:
           drx2.append(q)
           skip_sort='yes'
        else:
           drx3.append(q)

    drx=sorted(drx1)+sorted(drx2)+sorted(drx3)

    return {'return':0, 'list':drx, 'skip_sort':skip_sort}

##############################################################################
# get version from path

def version_cmd(i):

    ck=i['ck_kernel']

    fp=i['full_path']

    ver=''

    p1=os.path.dirname(fp)
    p2=os.path.dirname(p1)
    p3=os.path.dirname(p2)
    p4=os.path.dirname(p3)

    fv=os.path.join(p2,'version.txt')
    if not os.path.isfile(fv):
       fv=os.path.join(p3,'version.txt')
    if not os.path.isfile(fv):
       fv=os.path.join(p4,'version.txt')
    if os.path.isfile(fv):
       rx=ck.load_text_file({'text_file':fv, 'split_to_list':'yes'})
       if rx['return']==0:
          lst=rx['lst']
          for q in lst:
              if q.lower().startswith('version='):
                 ver=q[8:]
                 break

    if ver=='':
       ver=os.path.basename(p3)
       if ver.lower().startswith('v'):
          ver=ver[1:]
       if ver!='' and not ver[0].isdigit():
          ver=''

    return {'return':0, 'cmd':'', 'version':ver}

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

    iv=i.get('interactive','')

    cus=i.get('customize',{})
    fp=cus.get('full_path','')

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    # Check platform
    hplat=hosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    env=i['env']

    pi=fp
    found=False
    while True:
       if os.path.isdir(os.path.join(pi,'lib')) or os.path.isdir(os.path.join(pi,'lib64')):
          found=True
          break
       pix=os.path.dirname(pi)
       if pix==pi:
          break
       pi=pix

    if not found:
       return {'return':1, 'error':'can\'t find root dir of this installation'}

    ############################################################
    # Setting environment depending on the platform
    if hplat=='win':
       pl=''
       pinc=''

       if fp!='':
          pl=os.path.dirname(fp)
          cus['path_lib']=pl

          pl1=os.path.dirname(pl)
          pl2=os.path.dirname(pl1)

          pi=''
          if os.path.isfile(os.path.join(pl1,'include','CL','opencl.h')):
             pi=pl1
          elif os.path.isfile(os.path.join(pl2,'include','CL','opencl.h')):
             pi=pl2

       pb=''

       se=cus.get('skip_ext','')

       if fp.lower().find('cuda')<0:
          # If Windows and not CUDA
          if remote=='yes': 
             if se=='yes':
                ext=''
             else:
                ext='android32'
                if tbits=='64': 
                   ext='android64'
          else:
             ext='x64'
             if tbits=='32': 
                ext='x86'

             pb=pi+'\\bin'
             if ext!='': pb+='\\'+ext
          if pl=='':
             pl=pi+'\\lib'
             if ext!='': pl+='\\'+ext

       else:
          # if Windows + CUDA
          if remote=='yes': 
             return {'return':1, 'error':'this software doesn\'t support Android'}
          else:
             ext='x64'
             if tbits=='32': 
                ext='Win32'

             pb=pi+'\\bin'
             if pl=='':
                pl=pi+'\\lib\\'+ext

       if pb!='': cus['path_bin']=pb
       if pl!='': cus['path_lib']=pl
       if pi!='': cus['path_include']=pi+'\\include'

       if remote=='yes': 
          cus['dynamic_lib']='libOpenCL.so'
       else:
          cus['static_lib']='OpenCL.lib'

       cus['include_name']='CL\\opencl.h'

    else:
       ### Linux ###
       lb=os.path.basename(fp)
       if lb=='': lb='libOpenCL.so'

       pl=os.path.dirname(fp)
       cus['path_lib']=pl

       pl1=os.path.dirname(pl)
       pl2=os.path.dirname(pl1)

       pb=''
       if os.path.isdir(os.path.join(pl1,'bin')):
          pb=pl1
       elif os.path.isdir(os.path.join(pl2,'bin')):
          pb=pl2

       if pb!='':
          cus['path_bin']=os.path.join(pb,'bin')

       pi=''
       if os.path.isfile(os.path.join(pl,'include','CL','opencl.h')):
          pi=pl
       elif os.path.isfile(os.path.join(pl1,'include','CL','opencl.h')):
          pi=pl1
       elif os.path.isfile(os.path.join(pl2,'include','CL','opencl.h')):
          pi=pl2

       if pi=='':
          if os.path.isfile('/usr/include/CL/opencl.h'):
             pi='/usr'
          elif os.path.isfile('/usr/local/include/CL/opencl.h'):
             pi='/usr/local'

       if pi!='':
          cus['path_include']=os.path.join(pi,'include')
          cus['include_name']='CL/opencl.h'

       cus['static_lib']=lb
       cus['dynamic_lib']=lb

       r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': hosd, 
         'lib_path': cus.get('path_lib','')})
       if r['return']>0: return r
       s += r['script']

    ep=cus.get('env_prefix','')
    if pi!='' and ep!='':
       env[ep]=pi

    if remote=='yes':
       cus['skip_copy_to_remote']='yes'

    env['CK_ENV_LIB_OPENCL_INCLUDE_NAME']=cus.get('include_name','')
    env['CK_ENV_LIB_OPENCL_STATIC_NAME']=cus.get('static_lib','')
    env['CK_ENV_LIB_OPENCL_DYNAMIC_NAME']=cus.get('dynamic_lib','')

    return {'return':0, 'bat':s}
