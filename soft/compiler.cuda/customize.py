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
    return {'return':0}

##############################################################################
# limit directories 

def limit(i):

    hosd=i.get('host_os_dict',{})
    tosd=i.get('target_os_dict',{})

    phosd=hosd.get('ck_name','')

    dr=i.get('list',[])
    drx=[]

    for q in dr:
        if q.find('.{')<0 and q.find('X11')<0 and q.find('/lib/')<0:
           drx.append(q)

    return {'return':0, 'list':drx}

##############################################################################
# parse software version

def parse_version(i):

    lst=i['output']

    ver=''

    for q in lst:
        q=q.strip()
        if q!='':
           j=q.find(' V')
           if j>=0:
              ver=q[j+2:]

              j=ver.find(' ')
              if j>=0:
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

    ver=i.get('version','')
    sver=i.get('version_split',[])

    cus=i['customize']
    env=i['env']

    host_d=i.get('host_os_dict',{})
    target_d=i.get('host_os_dict',{})

    tbits=target_d.get('bits','')

    winh=host_d.get('windows_base','')

    deps=i['deps']

    fp=cus.get('full_path','')

    ep=cus.get('env_prefix','')
    p1=''
    p2=''
    if ep!='' and fp!='':
       p1=os.path.dirname(fp)
       p2=os.path.dirname(p1)

       env[ep]=p2
       env[ep+'_BIN']=p1

    env['CUDA_PATH']=p2
    env['CUDA_HOME']=p2
    env['CUDA_INSTALL_DIR']=p2

    opt1='--relaxed-constexpr'
    if len(sver)>1 and ((sver[0]==7 and sver[1]>=5) or sver[0]>7):
       opt1='--expt-relaxed-constexpr'
    env['CK_OPT_RELAXED_CONSTEXPR']=opt1

    opt2=' '
    if len(sver)>0 and sver[0]>6:
       opt2='--std=c++11'
    env['CK_COMPILER_FLAG_CPP11']=opt2

    if p1!='':
       ############################################################
       if winh=='yes':
          s+='\nset PATH='+p1+';'+p2+'\\libnvvp;'+p2+'\\nnvm\\bin;'+p2+'\\open64\\bin;%PATH%\n\n'

          env['CK_COMPILER_FLAGS_OBLIGATORY']='-DWINDOWS'

          ext='x64'
          if tbits=='32':
             ext='Win32'

          env[ep+'_LIB']=p2+'\\lib\\'+ext
          env[ep+'_INCLUDE']=p2+'\\include'

          rx=ck.access({'action':'convert_to_cygwin_path',
                        'module_uoa':'os',
                        'path':p2})
          if rx['return']>0: return rx
          env[ep+'_WIN']=rx['path']
       else:
          s+='\nexport PATH='+p1+':$PATH\n\n'

          # Update -ccbin -> dep on GCC
          gcc=deps['gcc']['dict']['customize']
          y=gcc.get('full_path','')

          if y!='':
             x=env['CK_NVCC']
             if '-ccbin' not in x:
                env['CK_NVCC']=x+' -ccbin '+y

             x=env['CK_NVCXX']
             if '-ccbin' not in x:
                y=y.replace('gcc','g++')
                env['CK_NVCXX']=x+' -ccbin '+y

          lp=''
          if os.path.isdir(p2+'/lib64'):
             lp=p2+'/lib64'
          elif os.path.isdir(p2+'/lib'):
             lp=p2+'/lib'

          if lp!='':
             env[ep+'_LIB']=lp

             r = ck.access({'action': 'lib_path_export_script', 'module_uoa': 'os', 'host_os_dict': host_d, 
               'lib_path': lp})
             if r['return']>0: return r
             s += r['script']

          env[ep+'_INCLUDE']=p2+'/include'

    return {'return':0, 'bat':s}
