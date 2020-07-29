#! /bin/bash

function download {
  NAME=${1}
  URL=${2}

  echo ""
  echo "Downloading ${NAME} from '${URL}' ..."

  wget -c ${URL}/${NAME}

  if [ "${?}" != "0" ] ; then
    echo "Error: Downloading ${NAME} from '${URL}' failed!"
    exit 1
  fi
}

function uncompress {
  ARCH=${1}
  echo ""
  echo "Uncompress archive ..."

  gunzip ${ARCH}
  if [ "${?}" != "0" ] ; then
    echo "Error: uncompressing archive failed!"
    exit 1
  fi
}

# #####################################################################
mkdir -p ${INSTALL_TO}
cd ${INSTALL_TO}

download "${TRAIN_IMAGES}" ${DATASETS_URL}
uncompress "${TRAIN_IMAGES}"

download "${TRAIN_LABELS}" ${DATASETS_URL}
uncompress "${TRAIN_LABELS}"

download "${T10K_IMAGES}" ${DATASETS_URL}
uncompress "${T10K_IMAGES}"

download "${T10K_LABELS}" ${DATASETS_URL}
uncompress "${T10K_LABELS}"

# #####################################################################

exit 0
