#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Leo Gordon, leo@dividiti.com
#

import os
import re

##############################################################################
# a shell command to obtain the version

def version_cmd(i):

    full_path           = i['full_path']
    ver_detection_cmd   = "{0} --version >$#filename#$".format(full_path)

    return {'return': 0, 'cmd': ver_detection_cmd}


##############################################################################
# how to parse the version string out of the command above

def parse_version(i):

    first_line = i.get('output', [''])[0]

    match_obj       = re.match('GNU\s+Wget\s+(\d+\.\d+\.\d+)\s+', first_line)
    version_string  = match_obj.group(1) if match_obj else 'unknown'

    return {'return': 0, 'version': version_string}


##############################################################################
# setup the environment

def setup(i):

    cus                     = i['customize']
    full_path               = cus['full_path']

    path_bin                = os.path.dirname(full_path)
    path_install            = os.path.dirname(path_bin)

        # storing the "path_bin" in the "customize" section (higher level) :
    cus['path_bin']         = path_bin

        # storing the "path_install" in the environment (lower level) :
    env                         = i['env']
    env_prefix                  = cus['env_prefix']
    env[env_prefix]             = path_install
    env[env_prefix+'_BIN_FULL'] = full_path

    return {'return':0, 'bat':''}
