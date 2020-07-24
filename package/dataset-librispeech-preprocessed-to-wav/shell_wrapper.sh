#!/bin/bash

if [[ -v _DATASET_SUBSET ]] ; then
    $CK_ENV_COMPILER_PYTHON_FILE $PACKAGE_DIR/convert_librispeech.py \
                                                --input_dir "$CK_ENV_DATASET_LIBRISPEECH" \
                                                --dest_dir "$INSTALL_DIR" \
                                                --output_json "$INSTALL_DIR/wav-list.json" \
                                                --subset_list $PACKAGE_DIR/$_DATASET_SUBSET
else
    $CK_ENV_COMPILER_PYTHON_FILE $PACKAGE_DIR/convert_librispeech.py \
                                                --input_dir "$CK_ENV_DATASET_LIBRISPEECH" \
                                                --dest_dir "$INSTALL_DIR" \
                                                --output_json "$INSTALL_DIR/wav-list.json"
fi


