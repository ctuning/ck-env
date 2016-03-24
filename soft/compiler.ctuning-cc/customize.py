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
              cfg          - dict of the soft entry
              tags         - list of tags
              env          - environment
              deps         - resolved deps

              interactive  - if 'yes', ask questions

              (customize)  - external params for possible customization:

                             target_arm - if 'yes', target ARM
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat        - prepared string for bat file
            }

    """

    import os

    # Get variables
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

    envp=cus.get('env_prefix','')
    pi=cus.get('path_install','')

    ############################################################
    # Prepare environment
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
