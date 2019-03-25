#!/usr/bin/env python

#
# An example script entry (returns current ticker status of Kraken cryptocurrency exchange)
#
# Developer: Leo Gordon
#


from pprint import pprint
import sys


def show(i):
    """
    Input:  {
                (all input parameters are optional)
    }

    Output: {
                return      - return code =  0, if successful
                                          >  0, if error
                (error)     - error text if return > 0
    }

    Execution examples: {

        info.py             # run directly (default interpreter)
        python info.py      # (same, but does not require executable permission)

        python2   info.py   # run directly (specify interpreter)
        python2.7 info.py
        python3   info.py
        python3.6 info.py

        ck run script:debug @input1.json @input2.json                       # run via CK (default interpreter)

        CK_PYTHON=python2 ck run script:debug @input1.json @input2.json     # run via CK (specify interpreter)
        CK_PYTHON=python3 ck run script:debug @input1.json @input2.json

        ## Using experimental _run_external() method to run a script under any given Python:
        #
        ck _run_external script:debug @@@"{'prewrapper_lines': ['export CK_PYTHON=python3'], 'dict': {'alpha': 777}}" --keep_tmp_files
    }

    """

    if 'ck_kernel' in i:
        i['ck_kernel'] = str( i['ck_kernel'] )      # not serializable otherwise

    output_dict = {
        'input_params': i,
        'current_python':   {
            'executable_path':  str( sys.executable ),
            'version':          list( sys.version_info ),
            'effective_path':   sys.path,
        },
        'return': 0,
    }

    pprint(output_dict, indent=4)

    return output_dict


if __name__ == '__main__':      # a simple unit test

    show( {'foo': 'bar'} )
