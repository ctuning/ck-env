#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

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

    host_d=i.get('host_os_dict',{})
    target_d=i.get('target_os_dict',{})
    winh=host_d.get('windows_base','')
    win=target_d.get('windows_base','')
    remote=target_d.get('remote','')
    mingw=target_d.get('mingw','')
    tbits=target_d.get('bits','')

    sdirs=host_d.get('dir_sep','')

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    fp=cus.get('full_path','')
    p1=os.path.dirname(fp)
    pi=os.path.dirname(p1)

    pb=pi+sdirs+'bin'

    cus['path_bin']=pb

    ep=cus.get('env_prefix','')
    if pi!='' and ep!='':
       env[ep]=pi
       env[ep+'_BIN']=pb

    ############################################################
    # Prepare environment
    if winh=='yes':
       s='\n'
       s+='set CCC_ROOT='+pi+'\n'
       s+='set CCC_PLUGINS=%CCC_ROOT%\\src-plat-indep\n'
       s+='set PATH=%CCC_ROOT%\\src-plat-indep\\plugins;%PATH%\n'

       s+='set CTUNING_ANALYSIS_CC=%CK_ENV_COMPILER_GCC%\\bin\\gcc\n'
       s+='set CTUNING_ANALYSIS_CPP=%CK_ENV_COMPILER_GCC%\\bin\\g++\n'
       s+='set CTUNING_ANALYSIS_FORTRAN=%CK_ENV_COMPILER_GCC%\\bin\\gfortran\n'

       s+='\n'
       s+='set CTUNING_COMPILER_CC=%CK_CC%\n'
       s+='set CTUNING_COMPILER_CPP=%CK_CXX%\n'
       s+='set CTUNING_COMPILER_FORTRAN=%CK_FC%\n'

       s+='\n'
       s+='if "%CK_CC%" == "ctuning-cc" (\n'
       s+='  set CTUNING_COMPILER_CC=gcc\n'
       s+='  set CTUNING_COMPILER_CPP=g++\n'
       s+='  set CTUNING_COMPILER_FORTRAN=gfortran\n'
       s+=')\n'

       s+='\n'
       s+='set CK_MAKE=make\n'
       s+='set CK_OBJDUMP="objdump -d"\n'

       s+='\n'
       s+='rem PRESET SOME DEFAULT VARIABLES\n'
       s+='set ICI_PROG_FEAT_PASS=fre\n'

       s+='\n'
       s+='rem set cTuning web-service parameters\n'
       s+='set CCC_CTS_URL=cTuning.org/wiki/index.php/Special:CDatabase?request=\n'
       s+='rem set CCC_CTS_URL=localhost/cTuning/wiki/index.php/Special:CDatabase?request=\n'
       s+='set CCC_CTS_DB=fursinne_coptcases\n'
       s+='rem set cTuning username (self-register at http://cTuning.org/wiki/index.php/Special:UserLogin)\n'
       s+='set CCC_CTS_USER=gfursin\n'

       s+='\n'
       s+='rem compiler which was used to extract features for all programs to keep at cTuning.org\n'
       s+='rem do not change it unless you understand what you do ;) ...\n'
       s+='set CCC_COMPILER_FEATURES_ID=129504539516446542\n'

       s+='\n'
       s+='rem use architecture flags from cTuning\n'
       s+='set CCC_OPT_ARCH_USE=0\n'

       s+='\n'
       s+='rem retrieve opt cases only when execution time > TIME_THRESHOLD\n'
       s+='set TIME_THRESHOLD=0.3\n'

       s+='\n'
       s+='rem retrieve opt cases only with specific notes\n'
       s+='rem set NOTES=\n'

       s+='\n'
       s+='rem retrieve opt cases only when profile info is !=""\n'
       s+='rem set PG_USE=1\n'

       s+='\n'
       s+='rem retrieve opt cases only when execution output is correct (or not if =0)\n'
       s+='set OUTPUT_CORRECT=1\n'

       s+='\n'
       s+='rem check user or total execution time\n'
       s+='rem set RUN_TIME=RUN_TIME_USER\n'
       s+='set RUN_TIME=RUN_TIME\n'

       s+='\n'
       s+='rem Sort optimization case by speedup (0 - ex. time, 1 - code size, 2 - comp time)\n'
       s+='set SORT=012\n'

       s+='\n'
       s+='rem produce additional optimization report including optimization space froniters\n'
       s+='set CT_OPT_REPORT=1\n'

       s+='\n'
       s+='rem Produce optimization space frontier\n'
       s+='rem set DIM=01 (2D frontier)\n'
       s+='rem set DIM=02 (2D frontier)\n'
       s+='rem set DIM=12 (2D frontier)\n'
       s+='rem set DIM=012 (3D frontier)\n'
       s+='rem set DIM=012\n'

       s+='\n'
       s+='rem Cut cases when producing frontier (select cases when speedup 0,1 or 2 is more than some threshold)\n'
       s+='rem set CUT=0,0,1.2\n'
       s+='rem set CUT=1,0.80,1\n'
       s+='rem set CUT=0,0,1\n'

       s+='\n'
       s+='rem find similar cases from the following platform\n'
       s+='set CCC_PLATFORM_ID=2111574609159278179\n'
       s+='set CCC_ENVIRONMENT_ID=2781195477254972989\n'
       s+='set CCC_COMPILER_ID=331350613878705696\n'

    else:
       s='\n'
       s+='export CCC_ROOT='+pi+'\n'
       s+='export CCC_PLUGINS=$CCC_ROOT/src-plat-indep\n'
       s+='export PATH=$CCC_ROOT/src-plat-indep/plugins:$PATH\n'

       s+='export CTUNING_ANALYSIS_CC=$CK_ENV_COMPILER_GCC/bin/gcc\n'
       s+='export CTUNING_ANALYSIS_CPP=$CK_ENV_COMPILER_GCC/bin/g++\n'
       s+='export CTUNING_ANALYSIS_FORTRAN=$CK_ENV_COMPILER_GCC/bin/gfortran\n'

       s+='\n'
       s+='export CTUNING_COMPILER_CC=$CK_CC\n'
       s+='export CTUNING_COMPILER_CPP=$CK_CXX\n'
       s+='export CTUNING_COMPILER_FORTRAN=$CK_FC\n'

       s+='\n'
       s+='if [ "${CK_CC}" == "ctuning-cc" ] ; then\n'
       s+='  export CTUNING_COMPILER_CC=gcc\n'
       s+='  export CTUNING_COMPILER_CPP=g++\n'
       s+='  export CTUNING_COMPILER_FORTRAN=gfortran\n'
       s+='fi\n'

       s+='\n'
       s+='export CK_MAKE=make\n'
       s+='export CK_OBJDUMP="objdump -d"\n'

       s+='\n'
       s+='# PRESET SOME DEFAULT VARIABLES\n'
       s+='export ICI_PROG_FEAT_PASS=fre\n'

       s+='\n'
       s+='#set cTuning web-service parameters\n'
       s+='export CCC_CTS_URL=cTuning.org/wiki/index.php/Special:CDatabase?request=\n'
       s+='#export CCC_CTS_URL=localhost/cTuning/wiki/index.php/Special:CDatabase?request=\n'
       s+='export CCC_CTS_DB=fursinne_coptcases\n'
       s+='#set cTuning username (self-register at http://cTuning.org/wiki/index.php/Special:UserLogin)\n'
       s+='export CCC_CTS_USER=gfursin\n'

       s+='\n'
       s+='#compiler which was used to extract features for all programs to keep at cTuning.org\n'
       s+='#do not change it unless you understand what you do ;) ...\n'
       s+='export CCC_COMPILER_FEATURES_ID=129504539516446542\n'

       s+='\n'
       s+='#use architecture flags from cTuning\n'
       s+='export CCC_OPT_ARCH_USE=0\n'

       s+='\n'
       s+='#retrieve opt cases only when execution time > TIME_THRESHOLD\n'
       s+='export TIME_THRESHOLD=0.3\n'

       s+='\n'
       s+='#retrieve opt cases only with specific notes\n'
       s+='#export NOTES=\n'

       s+='\n'
       s+='#retrieve opt cases only when profile info is !=""\n'
       s+='#export PG_USE=1\n'

       s+='\n'
       s+='#retrieve opt cases only when execution output is correct (or not if =0)\n'
       s+='export OUTPUT_CORRECT=1\n'

       s+='\n'
       s+='#check user or total execution time\n'
       s+='#export RUN_TIME=RUN_TIME_USER\n'
       s+='export RUN_TIME=RUN_TIME\n'

       s+='\n'
       s+='#Sort optimization case by speedup (0 - ex. time, 1 - code size, 2 - comp time)\n'
       s+='export SORT=012\n'

       s+='\n'
       s+='#produce additional optimization report including optimization space froniters\n'
       s+='export CT_OPT_REPORT=1\n'

       s+='\n'
       s+='#Produce optimization space frontier\n'
       s+='#export DIM=01 (2D frontier)\n'
       s+='#export DIM=02 (2D frontier)\n'
       s+='#export DIM=12 (2D frontier)\n'
       s+='#export DIM=012 (3D frontier)\n'
       s+='#export DIM=012\n'

       s+='\n'
       s+='#Cut cases when producing frontier (select cases when speedup 0,1 or 2 is more than some threshold)\n'
       s+='#export CUT=0,0,1.2\n'
       s+='#export CUT=1,0.80,1\n'
       s+='#export CUT=0,0,1\n'

       s+='\n'
       s+='#find similar cases from the following platform\n'
       s+='export CCC_PLATFORM_ID=2111574609159278179\n'
       s+='export CCC_ENVIRONMENT_ID=2781195477254972989\n'
       s+='export CCC_COMPILER_ID=331350613878705696\n'

    return {'return':0, 'bat':s, 'env':env, 'tags':tags}
