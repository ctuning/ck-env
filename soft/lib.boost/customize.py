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
# get version from path

def version_cmd(i):

    ck=i['ck_kernel']

    fp=i['full_path']

    ver=''

    p0=os.path.basename(fp)
    lib_prefix = '.lib'
    if p0.endswith(lib_prefix):
      # windows naming: libboost_system-vc140-mt-s-1_62.lib
      last_dash_index = p0.rfind('-')
      if -1 < last_dash_index:
        ver = p0[last_dash_index+1:-len(lib_prefix)].replace('_', '.')
    else:
      p1=os.path.dirname(fp)
      lst=os.listdir(p1)
      for fn in lst:
          if fn.startswith(p0):
             x=fn[len(p0):]
             if x.startswith('.'):
                ver=x[1:]
                break

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
    import glob

    # Get variables
    ck=i['ck_kernel']

    iv=i.get('interactive','')

    cus=i.get('customize',{})
    fp=cus.get('full_path','')

    p0=os.path.basename(fp)
    p1=os.path.dirname(fp)
    pi=os.path.dirname(p1)

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    file_extensions = hosd.get('file_extensions',{})

    win=tosd.get('windows_base','')
    winh=hosd.get('windows_base','')

    # Check platform
    hplat=hosd.get('ck_name','')
    tplat=tosd.get('ck_name','')
    ttags=tosd.get('tags',[])

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    env=i['env']
    sver=i['version_split']

    ep=cus['env_prefix']

    x=''
    if len(sver)>1:
       x=str(sver[0])+'.'+str(sver[1])
       env[ep+'_SHORT_VER']=x

    x=''
    j=0
    for y in sver:
        j+=1
        if x!='': x+='.'
        x+=str(y)
        if j==3: break
    if x!='':
       env[ep+'_VER']=x

    found=False
    lib_path = pi
    include_path = pi
    while not found:
       for p in glob.glob(os.path.join(pi,'lib*')):
         if os.path.isdir(p):
            lib_path = p
            break

       include_path = pi
       for p in glob.glob(os.path.join(pi,'include')):
         if os.path.isdir(p):
            include_path = p
            break

       found = '' != lib_path and '' != include_path

       if not found:
         lib_path = ''
         include_path = ''
         pix=os.path.dirname(pi)
         if pix==pi:
            break
         pi=pix

    if not found:
       return {'return':1, 'error':'can\'t find root dir of Boost installation'}

    env[ep]=pi

    cus['path_lib']=lib_path
    cus['path_include']=include_path

    r = ck.access({'action': 'lib_path_export_script', 
                   'module_uoa': 'os', 
                   'host_os_dict': hosd, 
                   'lib_path': cus.get('path_lib', '')})
    if r['return']>0: return r
    shell_setup_script_contents = r['script']

    ############################################################
    # Setting environment depending on the platform
    if tplat=='win':
       # Check if has dll and then add to PATH
       fpd=fp
       if fp.endswith('.lib'):
          fpd=fp[:-4]+'.dll'
       if fpd.endswith('.dll') and os.path.isfile(fpd):
          shell_setup_script_contents += '\nset PATH='+p1+';%PATH%\n\n'

       compiler = p0[len('libboost_system'):p0.find('-mt')]
       ver_suffix = p0[p0.find('-mt')+3:-len('.lib')]

       # TBD: we should actually go through existing libs and create vars automatically 
       env[ep+'_LFLAG_SYSTEM']=os.path.join(p1,'boost_system' + compiler + '-mt' + ver_suffix + '.lib')
       env[ep+'_LFLAG_THREAD']=os.path.join(p1,'boost_thread' + compiler + '-mt' + ver_suffix + '.lib')
       env[ep+'_LFLAG_DATE_TIME']=os.path.join(p1,'boost_date_time' + compiler + '-mt' + ver_suffix + '.lib')
       env[ep+'_LFLAG_FILESYSTEM']=os.path.join(p1,'boost_filesystem' + compiler + '-mt' + ver_suffix + '.lib')
       env[ep+'_LFLAG_REGEX']=os.path.join(p1,'boost_regex' + compiler + '-mt' + ver_suffix + '.lib')
    else:
       env[ep+'_LFLAG_SYSTEM']='-lboost_system'
       env[ep+'_LFLAG_THREAD']='-lboost_thread'
       env[ep+'_LFLAG_DATE_TIME']='-lboost_date_time'
       env[ep+'_LFLAG_FILESYSTEM']='-lboost_filesystem'
       env[ep+'_LFLAG_REGEX']='-lboost_regex'

    for python_ver_suffix in ('', '3'):
        python_library_path_candidate = os.path.join(lib_path, 'libboost_python' + python_ver_suffix + file_extensions.get('dll',''))
        if os.path.exists( python_library_path_candidate ):
            env[ep + '_PYTHON_LIBRARY'] = python_library_path_candidate

    # Check if host is windows and target is android
    # then copy libboost_thread_pthread.a to libboost_thread.a ,
    # otherwise other soft may not understand that ...
    if hplat=='win' and 'android' in ttags:
       px0=os.path.join(p1,'libboost_thread_pthread.a')
       if os.path.isfile(px0):
          px1=os.path.join(p1,'libboost_thread.a')
          if os.path.isfile(px1):
             os.remove(px1)
          import shutil
          shutil.copyfile(px0,px1)

       shell_setup_script_contents += '\nset LD_LIBRARY_PATH='+p1+':%LD_LIBRARY_PATH%\n\n'

    return {'return':0, 'bat':shell_setup_script_contents }
