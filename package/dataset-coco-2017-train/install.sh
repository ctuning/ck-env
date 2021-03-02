#! /bin/bash

function download {
  NAME=${1}
  URL=${2}
  ARCH=${3}
  FULL_URL=${URL}/${ARCH}
  echo ""
  echo "Downloading ${NAME} from '${FULL_URL}' ..."

  wget -c ${FULL_URL} -O ${ARCH}

  if [ "${?}" != "0" ] ; then
    echo "Error: Downloading ${NAME} from '${FULL_URL}' failed!"
    exit 1
  fi
}

function uncompress {
  ARCH=${1}
  echo ""
  echo "Unzipping archive ..."

  unzip ${ARCH}
  if [ "${?}" != "0" ] ; then
    echo "Error: unzipping package failed!"
    exit 1
  fi
}

# #####################################################################

TRAIN_DATASET_NAME="COCO 2017 training dataset"
download "${TRAIN_DATASET_NAME}" ${IMAGE_URL} "${TRAIN_IMAGE_ARCHIVE}"
uncompress "${TRAIN_IMAGE_ARCHIVE}" && rm "${TRAIN_IMAGE_ARCHIVE}"

# #####################################################################

TRAINVAL_OBJ_INSTANCES_NAME="COCO 2017 Train/Val object instances"
download "${TRAINVAL_OBJ_INSTANCES_NAME}" ${ANNOTATION_URL} "${TRAINVAL_OBJ_INSTANCES_ARCHIVE}"
uncompress "${TRAINVAL_OBJ_INSTANCES_ARCHIVE}" && rm "${TRAINVAL_OBJ_INSTANCES_ARCHIVE}"

exit 0
