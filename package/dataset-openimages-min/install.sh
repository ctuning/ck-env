#! /bin/bash

function download {
  NAME=${1}
  URL=${2}

  echo ""
  echo "Downloading ${NAME} from '${URL}' ..."

  wget -c ${URL}

  if [ "${?}" != "0" ] ; then
    echo "Error: Downloading ${NAME} from '${URL}' failed!"
    exit 1
  fi
}

function uncompress {
  ARCH=${1}
  echo ""
  echo "Uncompress archive ..."

  tar zxvf ${ARCH}
  if [ "${?}" != "0" ] ; then
    echo "Error: uncompressing archive failed!"
    exit 1
   else
    rm ${ARCH}
  fi
}

# #####################################################################

VAL_IMG_NAME="OpenImages 2018 minimal dataset"
download "${VAL_IMG_NAME}" ${IMAGE_URL}
uncompress "${VAL_IMAGE_ARCHIVE}"

# #####################################################################

ANNOTATIONS_NAME="OpenImages 2018 minimal annotations"
download "${ANNOTATIONS_NAME}" ${ANNOTATION_URL}

# #####################################################################

CLASSES_NAME="OpenImages 2018 minimal classes"
download "${CLASSES_NAME}" ${CLASSES_URL}

exit 0
