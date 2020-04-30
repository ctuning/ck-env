#! /bin/bash

VAL_FILE_OUT=${INSTALL_DIR}/${CK_CALIBRATION_VAL_MAP_FILE}
VAL_FILE_REF=$(basename ${CK_CAFFE_IMAGENET_VAL_TXT})

if [ "${PACKAGE_VERSION}" == "first.500" ] || [ "${PACKAGE_VERSION}" == "all.500" ]; then

  # Take the file list from the aux directory and truncate it to the first 500 files.
  head -n 500 ${CK_ENV_DATASET_IMAGENET_AUX}/${VAL_FILE_REF} > ${VAL_FILE_OUT}

elif [ "${PACKAGE_VERSION}" == "mlperf.option1" ] || [ "${PACKAGE_VERSION}" == "mlperf.option2" ]; then

  # Copy the file list verbatim.
  cp ${ORIGINAL_PACKAGE_DIR}/${CK_CALIBRATION_IMAGE_LIST_IN} ${VAL_FILE_OUT}

else # general case

  # Match up the class labels with the image names and output to a val map file.
  awk 'NR==FNR{a[$1]=$2}NR>FNR{{print $1,a[$1]}}' \
      ${CK_ENV_DATASET_IMAGENET_AUX}/${VAL_FILE_REF} \
      ${ORIGINAL_PACKAGE_DIR}/${CK_CALIBRATION_IMAGE_LIST_IN} \
      > ${VAL_FILE_OUT}

fi

# Copy the image files based on the val map.
while read LINE; do
  FILENAME=$(echo $LINE | cut -d' ' -f 1)
  cp  ${CK_ENV_DATASET_IMAGENET_VAL}/${FILENAME} ${INSTALL_DIR}
done < ${VAL_FILE_OUT}

echo "Done."
exit 0
