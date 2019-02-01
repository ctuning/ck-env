#! /bin/bash

unset EASYBUILD_PREFIX
unset EBDEVELEASYBUILD
unset EBROOTEASYBUILD
unset EBVERSIONEASYBUILD
unset LOADEDMODULES

cd $INSTALL_DIR

#module unload EasyBuild

# From https://easybuild.readthedocs.io/en/latest/Installation.html#installing-easybuild

# pick an installation prefix to install EasyBuild to (change this to your liking)
EASYBUILD_PREFIX=$INSTALL_DIR

# download script
curl -O https://raw.githubusercontent.com/easybuilders/easybuild-framework/develop/easybuild/scripts/bootstrap_eb.py

# bootstrap EasyBuild
python bootstrap_eb.py $EASYBUILD_PREFIX

# update $MODULEPATH, and load the EasyBuild module
#module use $EASYBUILD_PREFIX/modules/all
#module load EasyBuild
