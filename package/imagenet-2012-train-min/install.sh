#! /bin/bash

#
# Installation script for the 2012 ImageNet Large Scale Visual Recognition
# Challenge (ILSVRC'12) train dataset.
#
# See CK LICENSE for licensing details.
# See CK COPYRIGHT for copyright details.
#
# Developer(s):
# - Grigori Fursin, Grigori.Fursin@cTuning.org, 2018

# PACKAGE_DIR
# INSTALL_DIR

IMAGENET_TRAIN_TAR=${INSTALL_DIR}/ILSVRC2012_img_train.tar

#####################################################################
echo ""
echo "Checking whether '${IMAGENET_TRAIN_TAR}' already exists ..."
if [ -f "${IMAGENET_TRAIN_TAR}" ]
then
  echo "${IMAGENET_TRAIN_TAR} already exists ..."
  exit 1
fi

#####################################################################
echo ""
echo "Downloading ILSVRC'12 train dataset from '${IMAGENET_TRAIN_URL}' ..."

wget --no-check-certificate -c ${IMAGENET_TRAIN_URL} -O ${IMAGENET_TRAIN_TAR}
if [ "${?}" != "0" ] ; then
  echo "Error: Downloading ILSVRC'12 train set from '${IMAGENET_TRAIN_URL}' failed!"
  exit 1
fi

#####################################################################
echo ""
echo "Calculating the MD5 hash of '${IMAGENET_TRAIN_TAR}' ..."
IMAGENET_TRAIN_MD5_CALC=($(${CK_MD5SUM_CMD} ${IMAGENET_TRAIN_TAR}))
if [ "${?}" != "0" ] ; then
  echo "Error: Calculating the MD5 hash of '${IMAGENET_TRAIN_TAR}' failed!"
  exit 1
fi

#####################################################################
echo ""
echo "Validating the MD5 hash of '${IMAGENET_TRAIN_TAR}' ..."
echo "Calculated MD5 hash: ${IMAGENET_TRAIN_MD5_CALC}"
echo "Reference MD5 hash: ${IMAGENET_TRAIN_MD5}"
if [ "${IMAGENET_TRAIN_MD5_CALC}" != "${IMAGENET_TRAIN_MD5}" ] ; then
  echo "Error: Validating the MD5 hash of '${IMAGENET_TRAIN_TAR}' failed!"
  exit 1
fi

#####################################################################
echo ""
echo "Unpacking '${IMAGENET_TRAIN_TAR}' ..."

cd ${INSTALL_DIR}
tar xvf ${IMAGENET_TRAIN_TAR}
if [ "${?}" != "0" ] ; then
  echo "Error: Unpacking '${IMAGENET_TRAIN_TAR}' failed!"
  exit 1
fi

######################################################################
#echo ""
#echo "Removing '${IMAGENET_TRAIN_TAR}' ..."
#
#cd ${INSTALL_DIR}
#rm ${IMAGENET_TRAIN_TAR}
#if [ "${?}" != "0" ] ; then
#  echo "Error: Removing '${IMAGENET_TRAIN_TAR}' failed!"
#  exit 1
#fi

#####################################################################
echo ""
echo "Extracting individual classes ..."

cd ${INSTALL_DIR}
for f in n*.tar; do
  dir="${f%.*}"
  echo $dir
  mkdir $dir
  tar xvf $f -C $dir
  rm $f
done

#####################################################################
echo ""
echo "Successfully installed the ILSVRC'12 train dataset ..."
exit 0
