#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#

import os

##############################################################################

def version_cmd(i):

    # The concept of version is not generally applicable to credentials

    return {'return':0, 'cmd':'', 'version':'N/A'}


##############################################################################

def setup(i):
    """
    Input:  {
              ck_kernel             - import CK kernel module (to reuse functions)

              customize             - updated customize vars from meta

              customize.env_mapping - the structure of the dialogue

              env                   - updated environment vars from meta

              interactive           - if 'yes', can ask questions, otherwise quiet and assume defaults
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    ck                  = i['ck_kernel']
    interactive_bool    = i.get('interactive', '') == 'yes'
    env_mapping         = i.get('customize', {}).get('env_mapping', [])
    env                 = i['env']                      # target structure to deposit the future environment variables

    for one_var_mapping in env_mapping:
        var_name = one_var_mapping['variable']

        # 1) Command line parameters have the highest precedence,
        # 2) followed by the variables of the current environment
        # 3) interactive ? interaction : default ? default : error
        var_value = env.get(var_name) or os.environ.get(var_name)

        if not var_value:
            default_value   = one_var_mapping.get('default_value')

            if interactive_bool:    # ask the question and collect the response:

                display_name = one_var_mapping['display_name']
                question = 'Please enter {}{}: '.format(display_name, " [hit return to accept the default '{}']".format(default_value) if default_value else '')
                kernel_ret = ck.inp({'text': question})
                if kernel_ret['return']:
                    return kernel_ret
                else:
                    var_value = kernel_ret['string']

                    if var_value=='' and default_value!=None:
                        var_value = default_value

            elif default_value!=None:   # assume the default
                var_value = default_value

            else:
                return {'return':1, 'error':'Non-interactive mode and no default for {} - bailing out'.format(var_name)}
        env[var_name] = var_value

        # Can add some general type checks and constraints if necessary (in response to "nonempty", "is_a_number", etc)

    return {'return':0, 'bat':''}
