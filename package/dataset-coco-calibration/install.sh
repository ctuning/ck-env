#! /bin/bash

# Will copy the images under this subdirectory to reuse existing soft:dataset.coco.2017.train,
# rather than to create a separate soft:dataset.coco.calibration.
TARGET_DIR="${INSTALL_DIR}/${TRAIN_DIR}"
mkdir -p ${TARGET_DIR}

# Copy the image files based on the file list.
while read LINE; do
  FILENAME=$(echo ${LINE} | cut -d' ' -f 1)
  cp  "${CK_ENV_DATASET_IMAGE_DIR}/${FILENAME}" ${TARGET_DIR}
done < "${PACKAGE_DIR}/${CK_CALIBRATION_IMAGE_LIST_IN}"

# Copy the file list itself.
cp "${PACKAGE_DIR}/${CK_CALIBRATION_IMAGE_LIST_IN}" "${INSTALL_DIR}/${CK_CALIBRATION_VAL_MAP_FILE}"

echo "Done."
exit 0
