#
# Collective Knowledge workflow framework
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

##############################################################################
# customize installation (via redirect)

def setup(i):
    ck=i['ck_kernel']

    # Find entry with script to reuse
    r=ck.access({'action':'find', 'cid':'package:tool-bazel-0.4.4-universal'})
    if r['return']>0: return r

    ppp=r['path']

    r=ck.load_module_from_path({'path':ppp, 'module_code_name':'custom', 'skip_init':'yes'})
    if r['return']>0: return r

    script=r['code']

    return script.setup(i)
