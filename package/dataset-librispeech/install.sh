#! /bin/bash

function download {

  NAME=${1}
  URL=${2}
  ARCH=${3}
  MD5_EXP=${4}
  FULL_URL=${URL}/${ARCH}

  echo ""
  echo "Downloading ${NAME} from '${FULL_URL}' ..."

  wget -c ${FULL_URL} -O ${ARCH}

  if [ "${?}" != "0" ] ; then
    echo "Error: Downloading ${NAME} from '${FULL_URL}' failed!"
    exit 1
  fi

  MD5_CALC=$(md5sum ${ARCH})
  if [ "${MD5_CALC:0:32}" != "${MD5_EXP}" ] ; then
    echo "Error: MD5 of ${ARCH} is incorrect!"
    exit 1
  fi
}

function uncompress {
  ARCH=${1}
  echo ""
  echo "Untarring archive ..."

  tar -xzf ${ARCH}
  if [ "${?}" != "0" ] ; then
    echo "Error: untarring package failed!"
    exit 1
  fi
}

# #####################################################################

download "${DATASET_NAME}" ${DATASET_URL} "${DATASET_ARCHIVE}" "${DATASET_MD5}"
uncompress "${DATASET_ARCHIVE}" && rm "${DATASET_ARCHIVE}"

# #####################################################################

exit 0
