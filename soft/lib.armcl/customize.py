#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import re

def version_cmd(i):

    full_path           = i['full_path']
    ver_detection_cmd   = "strings {0} | grep arm_compute_version >$#filename#$".format(full_path)

    return {'return':0, 'cmd': ver_detection_cmd}


def parse_version(i):

    first_line = i.get('output',[''])[0]

    # Example output to be parsed:
    #
    # arm_compute_version=v18.11 Build options: {'benchmark_tests': '0', 'neon': '1', 'validation_tests': '0', 'extra_cxx_flags': '-fPIC', 'arch': 'arm64-v8a'} Git hash=3d2d44ef55ab6b08afda8be48301ce3c55c7bc67
    # arm_compute_version=v0.0-unreleased Build options: {'benchmark_tests': '0', 'neon': '1', 'validation_tests': '0', 'extra_cxx_flags': '-fPIC', 'arch': 'arm64-v8a'} Git hash=e46a7beb6b3d89b7cc6a96faeab19ee4478d4e2e

    match_obj       = re.match('arm_compute_version=v(\d+\.\d+[\-\w]*)\s+.+uild options:\s+({.+})', first_line)
    version_string  = match_obj.group(1) if match_obj else 'unknown'
    build_options   = eval(match_obj.group(2) if match_obj else '{}')

    if int(build_options.get('neon', '0')):
        version_string += '-neon'

    if int(build_options.get('opencl', '0')):
        version_string += '-opencl'

    return {'return':0, 'version': version_string}


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

    env=i.get('env',{})
    cfg=i.get('cfg',{})
    deps=i.get('deps',{})
    tags=i.get('tags',[])
    cus=i.get('customize',{})

    tosd=i.get('target_os_dict',{})
    win=tosd.get('windows_base','')
    remote=tosd.get('remote','')
    mingw=tosd.get('mingw','')
    tbits=tosd.get('bits','')

    envp=cus.get('env_prefix','')

    hosd=i.get('host_os_dict',{})
    sdirs=hosd.get('dir_sep','')

    tplat=tosd.get('ck_name','')

    fp=cus.get('full_path','')

    p1, pname = os.path.split(fp)
    pi        = os.path.dirname(p1)
    inst_root = os.path.dirname(pi)

    j=pname.rfind('.')
    if j>0:
       pname=pname[:j]

    ep=cus['env_prefix']
    env[ep]=inst_root

    path_lib=os.path.join(inst_root, 'install', 'lib')
    cus['path_lib']=path_lib

    path_include=os.path.join(inst_root, 'install', 'include')
    cus['path_include']=path_include
    cus['path_includes']=[path_include]

    psrc=os.path.join(inst_root,'src')
    if os.path.isdir(psrc):
        env[ep+'_SRC']=psrc
        cus['path_includes'].append(psrc)

        psrci=os.path.join(psrc,'include')
        if os.path.isdir(psrci):
            env[ep+'_SRC_INCLUDE']=psrci
            cus['path_includes'].append(psrci)

        pkernels=os.path.join(psrc,'src', 'core', 'CL', 'cl_kernels/')
        if os.path.isdir(pkernels):
            env[ep+'_CL_KERNELS']=pkernels

        stub_dir=os.path.join(psrc, 'build', 'opencl-1.2-stubs')
        if os.path.isdir(stub_dir):
            env[ep+'_CL_STUB_RPATH_LINK'] = '-Wl,--rpath-link=' + stub_dir

    ptests=os.path.join(psrc,'tests')
    if os.path.isdir(ptests):
       env[ep+'_TESTS']=ptests
       cus['path_includes'].append(ptests)

    putils=os.path.join(psrc,'utils')
    if os.path.isdir(putils):
       env[ep+'_UTILS']=putils
       cus['path_includes'].append(putils)

    ################################################################
    if win=='yes':
       if remote=='yes' or mingw=='yes':
          sext='.a'
          dext='.so'
       else:
          sext='.lib'
          dext='.dll'
    else:
       sext='.a'
       dext='.so'

    r = ck.access({'action': 'lib_path_export_script',
                   'module_uoa': 'os',
                   'host_os_dict': hosd,
                   'lib_path': cus.get('path_lib','')})
    if r['return']>0: return r
    s += r['script']

    for x in (pname, pname+'-static'):
      if os.path.isfile(os.path.join(path_lib, x)+sext):
          cus['static_lib']           = x + sext
          env[ep+'_STATIC_NAME']      = x + sext
          trunc_name = x[3:] if x.startswith('lib') else x
          env[ep+'_LFLAG']            = '-l'+trunc_name

    for x in (pname+'_core', pname+'_core-static'):
      if os.path.isfile(os.path.join(path_lib, x)+sext):
          env[ep+'_STATIC_CORE_NAME'] = x + sext
          trunc_name = x[3:] if x.startswith('lib') else x
          env[ep+'_LFLAG_CORE']       = '-l'+trunc_name

    x=os.path.join(path_lib, pname+dext)
    if os.path.isfile(x):
        cus['dynamic_lib']            = pname + dext
        env[ep+'_DYNAMIC_NAME']       = pname + dext

    x=os.path.join(path_lib, pname+'_core'+dext)
    if os.path.isfile(x):
        env[ep+'_DYNAMIC_CORE_NAME']  = pname + '_core' + dext

    return {'return':0, 'bat':s}
