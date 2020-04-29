#! /bin/bash

VAL_FILE_OUT=${INSTALL_DIR}/${CK_CALIBRATION_VAL_MAP_FILE}

if [ "${PACKAGE_VERSION}" == "first.500" ] || [ "${PACKAGE_VERSION}" == "all.500" ]; then

  # Take the file list from the aux directory and truncate it to the first 500 files.
  VAL_FILE_IN=$(basename ${CK_CAFFE_IMAGENET_VAL_TXT})
  head -n 500 ${CK_ENV_DATASET_IMAGENET_AUX}/${VAL_FILE_IN} > ${VAL_FILE_OUT}

else # Must be either mlperf.option1 or mlperf.option2.

  cp ${ORIGINAL_PACKAGE_DIR}/${CK_CALIBRATION_IMAGE_LIST_IN} ${VAL_FILE_OUT}

fi

# Copy the image files based on the val map.
while read LINE; do
  FILENAME=$(echo $LINE | cut -d' ' -f 1)
  cp  ${CK_ENV_DATASET_IMAGENET_VAL}/${FILENAME} ${INSTALL_DIR}
done < ${VAL_FILE_OUT}

echo "Done."
exit 0
