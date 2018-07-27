#!/bin/bash

if [ "$1" != "1" ]; then if [ "$CK_ENV_PYTHON_SIMPORT_SET" == "1" ]; then return; fi; fi

# Finding the path to the directory that contains THIS bash script,
# the solution borrowed from here:
#       https://stackoverflow.com/questions/4774054/reliable-way-for-a-bash-script-to-get-the-full-path-to-itself

PATH_TO_THIS_ENTRY_DIR="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"

echo Adding $PATH_TO_THIS_ENTRY_DIR to the PYTHONPATH ...

export PYTHONPATH=${PATH_TO_THIS_ENTRY_DIR}:${PYTHONPATH}

export CK_ENV_PYTHON_SIMPORT_SET=1
