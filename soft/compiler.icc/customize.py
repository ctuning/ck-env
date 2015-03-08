#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK Copyright.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://cTuning.org/lab/people/gfursin
#

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg          - dict of the soft entry
              tags         - list of tags
              env          - environment
              deps         - dependencies

              interactive  - if 'yes', ask questions

              (customize)  - external params for possible customization:

                             target_arm - if 'yes', target ARM
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
              env          - updated environment
              deps         - updated dependencies
              tags         - updated tags

              path         - install path
            }

    """

    import os

    s=''

    iv=i.get('interactive','')
    if iv=='yes': print ('')

    deps=i.get('deps',[])
    env=i.get('env',{})
    cfg=i.get('cfg',{})
    cus=i.get('customize',{})
    tags=i.get('tags',[])

    tbits=i.get('target_os_bits','')

    vs_shell=cus.get('vs_shell','')
    if vs_shell=='':
       if iv=='yes':
          vs_shell=raw_input('Choose Visual Studio Shell (vs2008shell or vs2013): ')
          vs_shell=vs_shell.strip().lower()

       if vs_shell=='':
          return {'return':1, 'error':'"vs_shell" in "customize" is not defined'}

    target_d=i.get('target_os_dict',{})
    wb=target_d.get('windows_base','')

    envp=cfg.get('env_prefix','')

    pi=i.get('path','')

    s+='\n'
    s+='rem Intel environment\n'

    yy='call "'+pi+'\\bin\\compilervars.bat" '

    if tbits=='32': yy+=' ia32'
    else: yy+=' intel64'

    s+=yy+' '+vs_shell+'\n\n'

    return {'return':0, 'bat':s, 'env':env, 'tags':tags, 'deps':deps}
