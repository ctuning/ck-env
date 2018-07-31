#!/bin/bash

# Finding the path to the directory that contains THIS bash script,
# the solution borrowed from here:
#       https://stackoverflow.com/questions/4774054/reliable-way-for-a-bash-script-to-get-the-full-path-to-itself

PATH_TO_THIS_ENTRY_DIR="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"
ALREADY_LOADED_NAME=CK_STATIC_ENV_`basename $PATH_TO_THIS_ENTRY_DIR | tr -cd '[:alnum:]_'`
ALREADY_LOADED_FLAG=${ALREADY_LOADED_NAME}

if [ "$1" != "1" ] && [ "$ALREADY_LOADED_FLAG" == "1" ]; then return; fi;

echo Adding $PATH_TO_THIS_ENTRY_DIR to the PYTHONPATH ...

export PYTHONPATH=${PATH_TO_THIS_ENTRY_DIR}:${PYTHONPATH}

export ${ALREADY_LOADED_NAME}=1
